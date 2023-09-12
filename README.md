# Pyplay

Pyplay is a little framework for writing acceptance tests inspired by the screenplay pattern. Because we want acceptance tests to be focused on behaviour of users, the analogy of a theatrical play is a really powerful one: every specification is a bit like a little play with characters doing things and expecting things.

## Play: the executable specification

An important aspect of acceptance tests is the distinction between the (executable) specification and the layer that translates these to actual interactions with the system under test. In pyplay, this distinction is made explicit. The specification is the _play_ and consists of a series of _actions_ performed by _characters_. The definition of a play looks like this:
```
character('Brian').performs(IncreaseCounter())
character('John').asserts(CounterEquals(1))
```
A special kind of action is the _assertion_: it is an action in which a character sets an explicit expectation.

## Play execution: the implementation

To execute the play, we need some more things. First, there are _actors_ that play the characters. Secondly, there is the _stage_ they are on. These are the two dependencies an executor of an action has:
```
async def increase_counter(action: IncreaseCounter, actor: Actor, stage: Stage) -> None:
    app = await stage.prop(App)
    app.increase_counter()
    actor.write_log_message(IncreasedCounter())
```
