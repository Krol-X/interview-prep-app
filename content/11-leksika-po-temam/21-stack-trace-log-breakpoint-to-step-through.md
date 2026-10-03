---
title: "stack trace, log, breakpoint, to step through"
hot: false
sub: "3. Баги, отладка, конкурентность"
---
- **stack trace / backtrace** — *The stack trace pointed to the serializer.*
- **log / logs / logging** — *I added logging around the call.* *log level: debug, info, warn, error.*
- **breakpoint** — точка останова: *I set a breakpoint in the callback.* (*binding.irb / byebug / pry*)
- **to step through** — пройти по шагам: *I stepped through the code in the debugger.*
- **to inspect** — посмотреть значение: *inspect the variable.*
- **to print-debug** (*puts debugging*) — честно и нормально.
- **exception / error / to raise / to rescue**, **to swallow an exception** (проглотить — плохо).
- **to crash / to hang / to time out**.

> The stack trace wasn't helpful, so I added logging, set a breakpoint, and stepped through the callback until I saw the job being enqueued before the commit.
