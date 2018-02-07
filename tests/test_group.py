# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import uuid
from random import randrange

import pytest

from pages.home_page import Home


class TestGroup:

    @pytest.mark.credentials
    def test_group_description_edit(self, base_url, selenium, vouched_user):
        home_page = Home(selenium, base_url).open()
        home_page.login(vouched_user['email'])

        # Create a new group
        group_name = 'moz-group-{0}'.format(uuid.uuid4())
        groups_page = home_page.header.click_groups_menu_item()
        group = groups_page.create_group(group_name)

        # New group data
        new_group_description = 'This is an automated group.'
        new_group_irc_channel = '#testgroup'

        # Update the group description fields
        group_description = group.description.description_info
        group_description.set_description(new_group_description)
        group_description.set_irc_channel(new_group_irc_channel)
        group_description.click_update()

        search_listings = home_page.header.search_for(group_name)
        group_info = search_listings.open_group(group_name)

        # Check that everything was updated
        assert new_group_description == group_info.description
        assert new_group_irc_channel == group_info.irc_channel

    @pytest.mark.credentials
    def test_group_deletion_confirmation(self, base_url, selenium, vouched_user):
        home_page = Home(selenium, base_url).open()
        home_page.login(vouched_user['email'])

        # Create a new group
        group_name = 'moz-group-{0}'.format(uuid.uuid4())
        groups_page = home_page.header.click_groups_menu_item()
        group = groups_page.create_group(group_name)

        # Delete should only work with acknowledgement
        delete_form = group.description.delete_group
        assert not delete_form.is_delete_button_enabled
        delete_form.check_acknowledgement()
        assert delete_form.is_delete_button_enabled
        groups_page = delete_form.click_delete_group()
        assert groups_page.is_group_deletion_alert_present

    @pytest.mark.credentials
    def test_group_type_change(self, base_url, selenium, vouched_user):
        home_page = Home(selenium, base_url).open()
        home_page.login(vouched_user['email'])

        # Create a new group
        group_name = 'moz-group-{0}'.format(uuid.uuid4())
        groups_page = home_page.header.click_groups_menu_item()
        group = groups_page.create_group(group_name)

        # Change group type to reveal criteria
        group_type = group.access.group_type
        assert not group_type.is_member_criteria_visible
        group_type.set_reviewed_group_type()
        assert group_type.is_member_criteria_visible

    @pytest.mark.credentials
    def test_group_invitations(self, base_url, selenium, vouched_user):
        home_page = Home(selenium, base_url).open()
        home_page.login(vouched_user['email'])

        # Create a new group
        group_name = 'moz-group-{0}'.format(uuid.uuid4())
        groups_page = home_page.header.click_groups_menu_item()
        group = groups_page.create_group(group_name)

        # Invite a new member
        invite = group.invitations.invite
        new_member = "Test User"
        invite.invite_new_member(new_member)
        invite.click_invite()

        # Check if the pending invitation exists
        invitations = group.invitations.invitations_list
        random_profile = randrange(len(invitations.search_invitation_list))
        assert new_member in invitations.search_invitation_list[random_profile].name

    @pytest.mark.credentials
    def test_github_non_nda_user_cannot_create_access_group(self, base_url, selenium, github_non_nda_user):
        home_page = Home(selenium, base_url).open()
        home_page.login_with_github(github_non_nda_user['username'], github_non_nda_user['password'],
                                    github_non_nda_user['secret'])
        groups_page = home_page.header.click_groups_menu_item()
        create_group_page = groups_page.click_create_group_main_button()
        assert not create_group_page.is_access_group_present
