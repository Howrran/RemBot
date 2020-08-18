"""Module for validators"""


class Validator():
    """
    Validators
    """

    @staticmethod
    def interval_validator(interval):
        """
        Validate new interval

        :param interval: int | interval in seconds
        :return:
        """
        if not interval.isnumeric():
            return False

        interval = int(interval)

        if not 1 < interval < 86_400:
            return False

        return True
