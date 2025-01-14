import unittest
from wagtail.actions.revert_to_page_revision import (
    RevertToPageRevisionAction,
    RevertToPageRevisionError,
    RevertToPageRevisionPermissionError,
)
from unittest.mock import Mock

class TestRevertToPageRevisionAction(unittest.TestCase):
    # CT1: Sem permissão para editar a página e revisão não necessária
    def test_no_permission_and_revision_not_needed(self):
        page = Mock(alias_of_id=None)
        user = Mock()
        user_permissions = Mock()
        user_permissions.can_edit.return_value = False
        page.permissions_for_user.return_value = user_permissions

        action = RevertToPageRevisionAction(
            page=page,
            revision=None,
            user=user,
        )

        with self.assertRaises(RevertToPageRevisionPermissionError):
            action.check(skip_permission_checks=False)
    
    # CT2: Com permissão para editar a página e revisão não necessária
    def test_permission_and_revision_not_needed(self):
        page = Mock(alias_of_id=None)
        user = Mock()
        user_permissions = Mock()
        user_permissions.can_edit.return_value = True
        page.permissions_for_user.return_value = user_permissions

        action = RevertToPageRevisionAction(
            page=page,
            revision=None,
            user=user,
        )

        action.check(skip_permission_checks=False)
    
    # CT3: Com permissão e ignorando verificações de permissão
    def test_permission_checks_skipped(self):
        page = Mock(alias_of_id=None)
        user = Mock()

        action = RevertToPageRevisionAction(
            page=page,
            revision=None,
            user=user,
        )

        action.check(skip_permission_checks=True)
    
    # CT4: Revisão necessária para página que é alias
    def test_revision_required_for_alias_page(self):
        page = Mock(alias_of_id=123)

        action = RevertToPageRevisionAction(
            page=page,
            revision=None,
            user=None,
        )

        with self.assertRaises(RevertToPageRevisionError):
            action.check(skip_permission_checks=False)
