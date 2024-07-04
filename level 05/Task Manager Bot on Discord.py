import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
import matplotlib.pyplot as plt
import aiofiles
import tempfile
from datetime import datetime, timedelta
import uuid

# Setup intents and bot instance
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Constants for file path and emoji mappings
TASKS_FILE = "tasks.json"
priority_emojis = {
    0: "🟢",
    1: "🟢",
    2: "🟢",
    3: "🟡",
    4: "🔴",
    5: "🔴"
}
status_emojis = {
    0: "0️⃣",  # Not Started
    1: "1️⃣",  # Initiated
    2: "2️⃣",  # In Progress
    3: "3️⃣",  # Near Completion
    4: "4️⃣",  # Completed
    5: "5️⃣"   # Closed
}
progress_emojis = {
    "0️⃣": 0,
    "1️⃣": 20,
    "2️⃣": 40,
    "3️⃣": 60,
    "4️⃣": 80,
    "5️⃣": 100
}

# Task list to store tasks
task_list = []

# Utility function to determine task status based on progress
def get_status_from_progress(progress):
    if progress == 0:
        return 0
    elif 1 <= progress <= 25:
        return 1
    elif 26 <= progress <= 50:
        return 2
    elif 51 <= progress <= 99:
        return 3
    elif progress == 100:
        return 4
    return 0

# Function to load tasks from a file
async def load_tasks():
    if os.path.exists(TASKS_FILE):
        async with aiofiles.open(TASKS_FILE, "r") as file:
            return json.loads(await file.read())
    return []

# Function to save tasks to a file
async def save_tasks():
    async with aiofiles.open(TASKS_FILE, "w") as file:
        await file.write(json.dumps(task_list))

# Function to calculate the next due date based on a recurrence pattern
def get_next_due_date(pattern):
    today = datetime.today()
    if pattern == "daily":
        return (today + timedelta(days=1)).strftime('%Y-%m-%d')
    elif pattern == "weekly":
        return (today + timedelta(weeks=1)).strftime('%Y-%m-%d')
    elif pattern == "monthly":
        return (today + timedelta(days=30)).strftime('%Y-%m-%d')
    return None

# Function to update recurring tasks
def update_recurring_tasks():
    today = datetime.today().strftime('%Y-%m-%d')
    for task in task_list:
        if task.get("is_recurring") and task["next_due_date"] <= today:
            task["progress"] = 0  # Reset progress
            task["next_due_date"] = get_next_due_date(task["recurrence_pattern"])

# Modal class for adding a new task
class AddTaskModal(discord.ui.Modal, title="Add New Task"):
    def __init__(self):
        super().__init__(timeout=None)
        self.task_type = discord.ui.TextInput(
            label="Task Type (main or extra)",
            placeholder="Enter task type (main or extra)",
            custom_id="task_type_input"
        )
        self.priority = discord.ui.TextInput(
            label="Priority (0-5, ignored for extra tasks)",
            placeholder="Enter task priority (0-5)",
            custom_id="priority_input"
        )
        self.description = discord.ui.TextInput(
            label="Task Description", 
            placeholder="Enter the task description", 
            style=discord.TextStyle.paragraph,
            custom_id="description_input"
        )
        self.is_recurring = discord.ui.TextInput(
            label="Is Recurring (yes or no)",
            placeholder="Enter if the task is recurring (yes or no)",
            custom_id="is_recurring_input"
        )
        self.recurrence_pattern = discord.ui.TextInput(
            label="Recurrence Pattern (daily, weekly, monthly)",
            placeholder="Enter the recurrence pattern (daily, weekly, monthly)",
            custom_id="recurrence_pattern_input"
        )
        self.add_item(self.task_type)
        self.add_item(self.priority)
        self.add_item(self.description)
        self.add_item(self.is_recurring)
        self.add_item(self.recurrence_pattern)

    # Function to handle the submission of the modal
    async def on_submit(self, interaction: discord.Interaction):
        task_type = self.task_type.value.lower()
        if task_type not in ["main", "extra"]:
            await interaction.response.send_message("Invalid task type! Use: main, extra.", ephemeral=True)
            return

        if task_type == "main":
            try:
                priority = int(self.priority.value)
            except ValueError:
                await interaction.response.send_message("Invalid priority! Use a number between 0 and 5.", ephemeral=True)
                return

            if priority not in range(6):
                await interaction.response.send_message("Invalid priority! Use a number between 0 and 5.", ephemeral=True)
                return
        else:
            priority = 0  # Extra tasks always have priority 0

        description = self.description.value
        is_recurring = self.is_recurring.value.lower() == "yes"
        recurrence_pattern = self.recurrence_pattern.value.lower()

        if is_recurring and recurrence_pattern not in ["daily", "weekly", "monthly"]:
            await interaction.response.send_message("Invalid recurrence pattern! Use: daily, weekly, monthly.", ephemeral=True)
            return

        new_task = {
            "id": str(uuid.uuid4()),  # Generate a unique ID for the task
            "description": description,
            "type": task_type,
            "priority": priority,
            "progress": 0,
            "is_recurring": is_recurring,
            "recurrence_pattern": recurrence_pattern if is_recurring else None,
            "next_due_date": get_next_due_date(recurrence_pattern) if is_recurring else None
        }
        task_list.append(new_task)
        await save_tasks()
        embed = discord.Embed(
            title="New Task Added",
            description=f"Task: **{description}**\nType: **{task_type.capitalize()}**\nPriority: **{priority_emojis[priority]} {priority}**\nProgress: **0%**",
            color=discord.Color.green()
        )
        embed.set_footer(text="Use /listtasks to see all tasks.")
        await interaction.response.send_message(embed=embed)

# Event handler for bot ready event
@bot.event
async def on_ready():
    global task_list
    task_list = await load_tasks()
    update_recurring_tasks()
    print(f'Bot {bot.user.name} is ready!')
    await bot.change_presence(activity=discord.Game(name="Managing Tasks"))
    await bot.tree.sync()
    task_reminders.start()

# Loop to send task reminders
@tasks.loop(minutes=1)
async def task_reminders():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    for task in task_list:
        if task["is_recurring"] and task["next_due_date"] == now.split(" ")[0]:
            channel = bot.get_channel(YOUR_CHANNEL_ID)  # Replace with your channel ID
            await channel.send(f"🔔 **Reminder:** Task **{task['description']}** is due today!")

# Command to add a new task
@bot.tree.command(name="addtask", description="Add a new task")
async def add_task(interaction: discord.Interaction):
    await interaction.response.send_modal(AddTaskModal())

# Command to list all current tasks
@bot.tree.command(name="listtasks", description="List all current tasks")
async def list_tasks(interaction: discord.Interaction):
    update_recurring_tasks()
    if task_list:
        for task in task_list:
            status = get_status_from_progress(task["progress"])
            embed = discord.Embed(
                title=f"Task ID: {task['id']}",
                description=(
                    f"**Description:** {task['description']}\n"
                    f"**Priority:** {priority_emojis[task['priority']]} {task['priority']}\n"
                    f"**Status:** {status_emojis[status]} {status}\n"
                    f"**Progress:** {task['progress']}%\n"
                    f"**Recurring:** {'Yes' if task.get('is_recurring') else 'No'}\n"
                    f"**Next Due Date:** {task.get('next_due_date', 'N/A')}"
                ),
                color=discord.Color.blue()
            )
            message = await interaction.channel.send(embed=embed)
            for emoji in progress_emojis.keys():
                await message.add_reaction(emoji)
    else:
        embed = discord.Embed(
            title="No Tasks Found",
            description="You don't have any tasks at the moment.",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)

# Event handler for reaction add event
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    message = reaction.message
    channel = message.channel

    # Extract task ID from the message embed title
    task_id = None
    if message.embeds:
        embed = message.embeds[0]
        if embed.title and embed.title.startswith("Task ID: "):
            task_id = embed.title[len("Task ID: "):]

    if task_id:
        task = next((task for task in task_list if task['id'] == task_id), None)
        if task and reaction.emoji in progress_emojis:
            task['progress'] = progress_emojis[reaction.emoji]
            await save_tasks()
            status = get_status_from_progress(task['progress'])
            embed = discord.Embed(
                title=f"Task ID: {task['id']}",
                description=(
                    f"**Description:** {task['description']}\n"
                    f"**Priority:** {priority_emojis[task['priority']]} {task['priority']}\n"
                    f"**Status:** {status_emojis[status]} {status}\n"
                    f"**Progress:** {task['progress']}%\n"
                    f"**Recurring:** {'Yes' if task.get('is_recurring') else 'No'}\n"
                    f"**Next Due Date:** {task.get('next_due_date', 'N/A')}"
                ),
                color=discord.Color.blue()
            )
            await message.edit(embed=embed)

# Command to remove a task
@bot.tree.command(name="removetask", description="Remove a task")
@app_commands.describe(task_id="The task ID to be removed")
async def remove_task(interaction: discord.Interaction, task_id: str):
    task = next((task for task in task_list if task['id'] == task_id), None)
    if task:
        task_list.remove(task)
        await save_tasks()
        embed = discord.Embed(
            title="Task Removed",
            description=f"Task **{task['description']}** has been removed.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Invalid Task ID",
            description="Please provide a valid task ID.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

# Command to clear all tasks (admin only)
@bot.tree.command(name="cleartasks", description="Remove all tasks (admins only)")
@app_commands.checks.has_permissions(administrator=True)
async def clear_tasks(interaction: discord.Interaction):
    global task_list
    task_list = []
    await save_tasks()
    embed = discord.Embed(
        title="All Tasks Removed",
        description="All tasks have been removed successfully.",
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed)

# Command to generate a productivity report
@bot.tree.command(name="productivityreport", description="Generate a productivity report")
async def productivity_report(interaction: discord.Interaction):
    update_recurring_tasks()
    if task_list:
        main_tasks = [task for task in task_list if task["type"] == "main"]
        completed_tasks = sum(1 for task in main_tasks if get_status_from_progress(task["progress"]) == 4)
        in_progress_tasks = sum(1 for task in main_tasks if get_status_from_progress(task["progress"]) in [1, 2, 3])
        not_started_tasks = sum(1 for task in main_tasks if get_status_from_progress(task["progress"]) == 0)

        total_tasks = len(main_tasks)
        completed_percentage = (completed_tasks / total_tasks) * 100
        in_progress_percentage = (in_progress_tasks / total_tasks) * 100
        not_started_percentage = (not_started_tasks / total_tasks) * 100

        # Generate bar chart
        labels = ["Completed", "In Progress", "Not Started"]
        counts = [completed_tasks, in_progress_tasks, not_started_tasks]
        colors = ["#4CAF50", "#FFC107", "#F44336"]

        plt.bar(labels, counts, color=colors)
        plt.xlabel("Status")
        plt.ylabel("Number of Tasks")
        plt.title("Productivity Report")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            plt.savefig(tmpfile.name)
            tmpfile.seek(0)
            file = discord.File(tmpfile.name, "report.png")

        embed = discord.Embed(
            title="Productivity Report",
            description=(
                f"Total Tasks: {total_tasks}\n"
                f"Completed: {completed_tasks} ({completed_percentage:.2f}%)\n"
                f"In Progress: {in_progress_tasks} ({in_progress_percentage:.2f}%)\n"
                f"Not Started: {not_started_tasks} ({not_started_percentage:.2f}%)"
            ),
            color=discord.Color.purple()
        )
        embed.set_image(url="attachment://report.png")

        await interaction.response.send_message(embed=embed, file=file)
        plt.clf()

    else:
        embed = discord.Embed(
            title="No Tasks Found",
            description="You don't have any tasks at the moment.",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)

# Command to show available commands
@bot.tree.command(name="helpme", description="Show available commands")
async def help_me(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Task Manager Commands",
        description="Here are the commands you can use:",
        color=discord.Color.purple()
    )
    embed.add_field(name="/addtask", value="Adds a new task.", inline=False)
    embed.add_field(name="/listtasks", value="Lists all current tasks.", inline=False)
    embed.add_field(name="/removetask <task ID>", value="Removes the specified task.", inline=False)
    embed.add_field(name="/updateprogress <task ID> <progress>", value="Updates the progress of the specified task.", inline=False)
    embed.add_field(name="/cleartasks", value="Removes all tasks (admins only).", inline=False)
    embed.add_field(name="/productivityreport", value="Generates a productivity report.", inline=False)
    await interaction.response.send_message(embed=embed)

# Run the bot with the token
bot.run('')
