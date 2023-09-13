# Pyplay

Pyplay is a little framework for writing acceptance tests inspired by the screenplay pattern.
Because we want acceptance tests to be focused on behaviour of users, the metaphor of a theatrical play is a really powerful one: every specification is a bit like a little play with characters doing things and expecting things.

## Play: the executable specification

An important aspect of acceptance tests is the distinction between the (executable) specification and the layer that translates these to actual interactions with the system under test.
In pyplay, this distinction is made explicit.
The specification is the _play_ and consists of a series of _actions_ performed by _characters_.
The definition of a play looks like this:
```
character('Brian').performs(IncreaseCounter())
character('John').asserts(CounterEquals(1))
```
A special kind of action is the _assertion_: it is an action in which a character sets an explicit expectation.

## Action execution: the implementation

To execute the play, all actions need to be executed.
An action executor is an `async def` with the `@executes` decorator to indicate that this function executes a certain action.
An action executor can use a certain set of dependencies to fulfil the execution.

### Stage props

The first dependency an action executor can use is _stage props_: these are objects available to all actors (objects "on stage"). These are accessed by type: 
```
@executes(IncreaseCounter)
async def increase_counter(stage_props: Props) -> None:
    app = await stage_props(App)
    app.increase_counter()
```

### Actor props

An action executor may also use the _actor_: this represents the person playing a character. An actor may also have _props_, they work the same as stage props, the difference being that actor props are unique for each actor and can only be accessed by that actor. A typical example would be a browser session:
```
@executes(IncreaseCounter)
async def increase_counter(actor: Actor) -> None:
    http_session = await actor.props(HttpSession)
    app.increase_counter()
```

### Log book

```
@executes(IncreaseCounter)
async def increase_counter(stage_props: Props, log_book: LogBook) -> None:
    app = await stage_props(App)
    app.increase_counter()
    log_book.write_message(IncreasedCounter())
```

### Character name

## Play execution
