import navigator


class UnknownEnvironment(Exception):
    pass


class Environment:
    available_navigators = {
        "rectangular_non_periodic": navigator.RectangularNonPeriodicNavigator,
        #  "rectangular_periodic": navigator.RectangularPeriodicNavigator,  # to be implemented
        #  "rectangular_partially_periodic": navigator.RectangularPartiallyPeriodicNavigator, # to be implemented
    }

    def __init__(self, style, dimensions, **kwargs):
        self.dimensions = dimensions
        if style not in self.available_navigators:
            error_message = f"{style} is not a recognized environment. currently implemented environments are: "
            error_message += " - ".join(self.available_navigators.keys())
            raise UnknownEnvironment(error_message)
        else:
            self.style = style
            self.navigator = self.available_navigators[self.style](
                **self.dimensions, **kwargs
            )

    def get_navigator(self):
        return self.navigator.get_replica()
