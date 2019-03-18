Issues reported on on [the project's repository issues page](https://github.com/own-dev/own-agent/issues) can 
have one or more of the following labels: `delighter`, `critical`, `enhancement`, `question`, `bug`, `duplicate`, 
`help wanted`, `invalid`, `wontfix`, and `to be tested and closed`, as well as labels with names of agents, 
e.g. `Science Agent`, `IP Agent`, etc.

`delighter` label state that issue is of low priority to the team.

`critical` label points out the higher priority of the issue for the team.

`question`, `bug`, and `enhancement` are the types of issues. 

`question` label means that the issue is more of a question than a request for new features or a report of broken features, but can sometimes lead to further discussion or changes of confusing or incongruous behavior or documentation.

`enhancement` issues describe points that can be improved in the way the system works at the moment of their report.  

`bug` issues documents broken, incorrect, or confusing behavior.

`duplicate` label points out that the issue is a duplicate of another reported issue.

`help wanted` label states that the issue appears to have a simple solution. Issues having this label should be a good starting place for new contributors to OWN Team.

`invalid` issues have been reviewed by a OWN developer, but they cannot be replicated even after the context specification.

`wontfix` label states that the issue is legitimate, but it is not something the OWN Team is currently able or willing to fix or implement. Issues having this label may be revisited in the future.


It is advised to label the issues with the name of the agent to which it is related, 
e.g. `Science Agent`, `IP Agent`, etc. To provide more context to the developers, 
and to be able to select all issues related to the corresponding agent.



As team members made necessary actions and consider the issue as resolved, they:
* commit those changes with the number of the issue, e.g. "#1", in the commits name, 
so that github will link the solution to the issue;
* describe this solution (if needed) in the comment for the issue; and 
* label the issue as `to be tested and closed`.

Later on issues marked as `to be tested and closed` are reviewed by @denef, @AlNedorezov, and @asverasver, 
who check it, and either close it if the problem stated in issues description is fixed 
and if they are satisfied with the result, or, otherwise, remove label `to be tested and closed`, 
and state necessary changes in issues description.
