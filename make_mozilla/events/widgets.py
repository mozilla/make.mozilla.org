from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'


class SplitDateTimeWidget(forms.MultiWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        if attrs is not None:
            date_attrs = {}
            time_attrs = {}

            if 'date_class' in attrs:
                date_attrs['class'] = attrs.get('date_class')
                del attrs['date_class']
            if 'date_placeholder' in attrs:
                date_attrs['placeholder'] = attrs.get('date_placeholder')
                del attrs['date_placeholder']

            if 'time_class' in attrs:
                time_attrs['class'] = attrs.get('time_class')
                del attrs['time_class']
            if 'time_placeholder' in attrs:
                time_attrs['placeholder'] = attrs.get('time_placeholder')
                del attrs['time_placeholder']

            date_attrs = dict(attrs.items() + date_attrs.items())
            time_attrs = dict(attrs.items() + time_attrs.items())
        else:
            date_attrs = time_attrs = None

        widgets = (DateInput(attrs=date_attrs, format=date_format),
               TimeInput(attrs=time_attrs, format=time_format))

        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]
