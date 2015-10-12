# Goals

- I want this software to be developed _asynchronously_: so people can work on the project at different times. We are students. We are busy. We can't possibly all line up our schedule very well.

- I want as many people as possible to be able to contribute to this project. Even students who are just learning how to code should be able to contribute. I am borrowing this philosophy from (OpenHatch)[https://openhatch.org/].

- I would like to implement agile development, but it is hard to get everyone in a room at the same time for a scrum. And besides, our business goals aren't rapidly changing anyway. There are however a few ideas that I will borrow from agile.

# Methodology

- There is a project-backlog (perhaps a roadmap) containing vague goals. This is the long-term vision for the project. These may coordinate with release dates, if end users ask for it.

- The core developers takes the top few items from the project-backlog and splits them up into small, specific, granular tasks (just like in agile), and enters it into the task-backlog. For now, the github issues tracker will work as the task-backlog. Each task has a difficulty, an hour estimation, and a priority.

- Anybody can pick a task out of the task backlog and run with it. Such person is called a fly-by developer. In true agile development, an employee would assign tasks to themselves during scrum and a manager would approve it, giving the employee more responsibility over that task. But we can't have a real-time scrum, and we don't have full-time employees.

- A separate branch should be created for each task (borrowed from [feature-branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)). This lets us look through the git history and add or subtract features very easily.

- Once a fly-by developer thinks they have completed a feature (after checkin all unit-tests), they tell a core developer. The reviewer comments on the code and the contributor revises his code. The cycle continues until the reviewer is satisfied. Then the reviewer merges the branch into master.

# Guidelines

- Try to pick up tasks that you have the time to complete. This is why there are hour estimations.

- Try to make the codebase easy to understand. This doesn't just mean writing clean and commented code, although that helps. Moreso, this means designing the project such that each individual part is isolated. If a fly-by developer wants to help debug the UI, they don't have to sift through code that both processes data and displays the UI.

- Unit-tests are a high priority. When a fly-by developer contributes code, manually finding introduced bugs is hard. Running a unit-test suite to automatically see if that contribution broke anything is easy.
