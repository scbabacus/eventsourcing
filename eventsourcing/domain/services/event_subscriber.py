from eventsourcing.domain.model.events import subscribe


def subscribe_to(event_class):
    """ Annotation for wrapping up a custom event handler function and subscribe to a certain event type
    Args:
        event_class: DomainEvent class or its child classes that the handler function should subscribe to

    Example usage:
        # this example shows a custom handler that reacts to Todo.Created event and saves a projection of a Todo model object
        @subscribe_to(Todo.Created)
        def new_todo_projection(event):
            todo = TodoProjection(id=event.entity_id, title=event.title)
            todo.save()
    """

    def create_type_predicate():
        def event_type_predicate(event):
            return isinstance(event, event_class)
        return event_type_predicate

    def wrap(query_func):
        subscribe(create_type_predicate(), query_func)

        def query_func_wrapper(*args, **kwargs):
            query_func(*args, **kwargs)
        return query_func_wrapper
    return wrap