""" Instructor apis serializers. """

from django.contrib.auth.models import User  # lint-amnesty, pylint: disable=imported-auth-user
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework import serializers

from lms.djangoapps.instructor.access import ROLES

from .tools import get_student_from_identifier


class RoleNameSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer that describes the response of the problem response report generation API.
    """

    rolename = serializers.CharField(help_text=_("Role name"))

    def validate_rolename(self, value):
        """
        Check that the rolename is valid.
        """
        if value not in ROLES:
            raise ValidationError(_("Invalid role name."))
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ShowStudentExtensionSerializer(serializers.Serializer):
    """
    Serializer for validating and processing the student identifier.
    """
    student = serializers.CharField(write_only=True, required=True)
    def validate_student(self, value):
        """
        Validate that the student corresponds to an existing user.
        """
        try:
            user = get_student_from_identifier(value)
        except User.DoesNotExist:
            response_payload = {
                'student': value,
                'userDoesNotExist': True,
            }
            return response_payload

        return user
