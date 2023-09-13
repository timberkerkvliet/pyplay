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
The most trivial one is the action object itself:
```
@executes(PrintAMessage)
async def print_message(action: PrintAMessage) -> None:
    print(action.message)
```

### Stage props

An action executor can use _stage props_: these are objects that everyone can interact with (objects "on stage"). There is at most one object of each type on stage that can be accessed in each action executor like this:
```
@executes(IncreaseCounter)
async def increase_counter(stage_props: Props) -> None:
    app = await stage_props(App)
    app.increase_counter()
```

### Actor props

In addition to stage props, there are also _actor props_.
An _actor_ is the person that plays a certain character.
Actor props work the same as stage props, the difference being that actor props are unique for each actor and can only be accessed by that actor (objects that are "held" by that actor).
A typical example would be a browser session:
```
@executes(VisitGoogle)
async def increase_counter(actor: Actor) -> None:
    http_session = await actor.props(HttpSession)
    await http_session.get('google.com')
```

### Log book
Data that you get back from the system under test, might need to be used in later actions.
Action executors can use a _log book_ to store (and later retrieve) this data.
Suppose, for example, that someone creates a basket:
```
@executes(CreateBasket)
async def increase_counter(stage_props: Props, log_book: LogBook) -> None:
    app = await stage_props(App)
    basket_id = await app.create_basket()
    log_book.write_message(CreatedBasket(basket_id))
```
The system under tests gives back an ID for the newly created basket, that we can use later if someone wants to assert that this basket is empty:
```
@executes(BasketIsEmpty)
async def increase_counter(stage_props: Props, log_book: LogBook) -> None:
    log_message = log_book.find().by_type(CreatedBasket).one()
    app = await stage_props(App)
    basket = app.get_basket(log_message.basket_id)
    assert basket.is_empty()
```
