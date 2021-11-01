import inject
from state import GlobalState


def setup_app() -> inject.Injector:
    def setup_inject(binder: inject.Binder) -> inject.Injector:
        binder.bind(GlobalState, GlobalState())

    injector = inject.clear_and_configure(config=setup_inject, bind_in_runtime=False)
    return injector
