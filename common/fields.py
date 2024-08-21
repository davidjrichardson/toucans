import json
from typing import Any
from django import forms
from django.db.models import JSONField
from django.forms import MultiValueField, MultiWidget, ValidationError, NumberInput


class LabelledNumberInput(NumberInput):
    template_name="home/widgets/labelled_number_input.html"

    def __init__(self, attrs=None, label=None) -> None:
        self.label = label
        super().__init__(attrs)

    def get_context(self, name: str, value: Any, attrs: dict[str, Any] | None) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        context["widget"]["label"] = self.label
        return context


class ArcheryLegResultWidget(MultiWidget):
    template_name = "home/widgets/archery_leg_result_widget.html"

    def __init__(self, attrs=None) -> None:
        widgets = (
            LabelledNumberInput(
                label="Score",
                attrs={
                    "placeholder": "Score",
                    "style": "border-top-right-radius: 0; border-bottom-right-radius: 0; border-right: 0;"
                }
            ),
            LabelledNumberInput(
                label="Hits",
                attrs={
                    "placeholder": "Hits",
                    "style": "border-radius: 0;"
                }
            ),
            LabelledNumberInput(
                label="Golds",
                attrs={
                    "placeholder": "Golds",
                    "style": "border-top-left-radius: 0; border-bottom-left-radius: 0; border-left: 0;"
                }
            ),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value: Any) -> Any:
        if value and type(value) == str:
            decoded_value = json.loads(value)
            return [
                decoded_value.get("score"), 
                decoded_value.get("hits"), 
                decoded_value.get("golds")
            ]
        
        return [None, None, None]


class ArcheryLegResultFormField(MultiValueField):
    default_error_messages = {
        "invalid_score": "Enter a valid score.",
        "invalid_hits": "Enter a valid number of hits.",
        "invalid_golds": "Enter a valid number of golds.",
    }
    widget = ArcheryLegResultWidget()

    def __init__(self, encoder=None, decoder=None, **kwargs) -> None:
        errors = self.default_error_messages.copy()
        fields = (
            forms.IntegerField(
                label="Score",
                error_messages={
                    "invalid": errors["invalid_score"],
                },
                min_value=0
            ),
            forms.IntegerField(
                label="Hits",
                error_messages={
                    "invalid": errors["invalid_hits"],
                },
                min_value=0
            ),
            forms.IntegerField(
                label="Golds",
                error_messages={
                    "invalid": errors["invalid_golds"],
                },
                min_value=0
            ),
        )

        if encoder and not callable(encoder):
            raise ValueError("The encoder parameter must be a callable object.")
        
        self.encoder = encoder

        if 'decoder' in kwargs:
            del kwargs['decoder']

        super().__init__(fields, **kwargs)

    def compress(self, data_list: Any) -> Any:
        if data_list:
            if data_list[0] in self.empty_values:
                raise ValidationError(
                    self.error_messages["invalid_score"],
                )
            if data_list[1] in self.empty_values:
                raise ValidationError(
                    self.error_messages["invalid_hits"],
                )
            if data_list[2] in self.empty_values:
                raise ValidationError(
                    self.error_messages["invalid_golds"],
                )
            string = json.dumps(
                {
                    "score": data_list[0],
                    "hits": data_list[1],
                    "golds": data_list[2],
                }, 
                cls=self.encoder
            )
            
            return string
        return None


class ArcheryLegResultField(JSONField):
    description = "Results of a league leg"

    def __init__(self, *args, **kwargs) -> None:
        super(ArcheryLegResultField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs: Any) -> Any:
        return super(ArcheryLegResultField, self).formfield(
            **{
                "form_class": ArcheryLegResultFormField,
                **kwargs,
            }
        )