import asyncio


# 1. async def and await
async def get_user():
    print("Getting user...")
    await asyncio.sleep(2)
    print("User received")
    return "Monish"


async def basic_await_example():
    print("Start")

    user = await get_user()

    print("User:", user)
    print("End")


# 2. asyncio.gather()
async def get_products():
    print("Getting products...")
    await asyncio.sleep(2)
    print("Products received")
    return ["Laptop", "Phone"]


async def gather_example():
    print("Starting multiple operations...")

    results = await asyncio.gather(
        get_user(),
        get_products(),
    )

    print("Results:", results)


# 3. asyncio.create_task()
async def send_email():
    print("Sending email...")
    await asyncio.sleep(2)
    print("Email sent")


async def create_task_example():
    print("Before creating task")

    task = asyncio.create_task(send_email())

    print("Normal code continues...")

    await task

    print("Task completed")


# 4. Event-loop behavior
async def first_task():
    print("First task started")
    await asyncio.sleep(2)
    print("First task finished")


async def second_task():
    print("Second task started")
    await asyncio.sleep(1)
    print("Second task finished")


async def event_loop_example():
    print("Starting tasks...")

    task1 = asyncio.create_task(first_task())
    task2 = asyncio.create_task(second_task())

    print("Both tasks are scheduled")

    await task1
    await task2

    print("All tasks completed")


# Main function
async def main():
    print("=== async def + await ===")
    await basic_await_example()

    print("\n=== asyncio.gather() ===")
    await gather_example()

    print("\n=== asyncio.create_task() ===")
    await create_task_example()

    print("\n=== Event Loop ===")
    await event_loop_example()


# Start the event loop
if __name__ == "__main__":
    asyncio.run(main())