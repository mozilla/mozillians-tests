# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import Base


class EditGroupPage(Base):
    _description_button_locator = (By.ID, 'description-tab')
    _description_tab_locator = (By.ID, 'description')
    _access_button_locator = (By.ID, 'access-tab')
    _access_tab_locator = (By.ID, 'access')
    _invitations_button_locator = (By.ID, 'invitations-tab')
    _invitations_tab_locator = (By.ID, 'invitations')

    @property
    def loaded(self):
        return self.is_element_displayed(*self._description_button_locator)

    @property
    def description(self):
        self.find_element(*self._description_button_locator).click()
        return self.DescriptionTab(self, self.find_element(*self._description_tab_locator))

    @property
    def access(self):
        self.find_element(*self._access_button_locator).click()
        return self.AccessTab(self, self.find_element(*self._access_tab_locator))

    @property
    def invitations(self):
        self.wait.until(expected.visibility_of_element_located(
            self._invitations_button_locator)).click()
        return self.InvitationsTab(self, self.find_element(*self._invitations_tab_locator))

    class DescriptionTab(Region):
        _description_form_locator = (By.ID, 'description-form')
        _delete_panel_locator = (By.CSS_SELECTOR, '.panel-danger')

        @property
        def description_info(self):
            return self.DescriptionForm(self.page, self.find_element(*self._description_form_locator))

        @property
        def delete_group(self):
            return self.DeletePanel(self.page, self.find_element(*self._delete_panel_locator))

        class DescriptionForm(Region):
            _description_locator = (By.ID, 'id_description')
            _irc_channel_locator = (By.ID, 'id_irc_channel')
            _update_locator = (By.ID, 'form-submit-description')

            def set_description(self, description_text):
                element = self.find_element(*self._description_locator)
                element.clear()
                element.send_keys(description_text)

            def set_irc_channel(self, irc_channel):
                element = self.find_element(*self._irc_channel_locator)
                element.clear()
                element.send_keys(irc_channel)

            def click_update(self):
                el = self.find_element(*self._update_locator)
                el.click()
                self.wait.until(expected.staleness_of(el))
                self.wait.until(expected.presence_of_element_located(
                    self._update_locator))

        class DeletePanel(Region):
            _delete_acknowledgement_locator = (By.ID, 'delete-checkbox')
            _delete_group_button_locator = (By.ID, 'delete-group')

            def check_acknowledgement(self):
                self.find_element(*self._delete_acknowledgement_locator).click()

            @property
            def is_delete_button_enabled(self):
                return 'disabled' not in self.find_element(*self._delete_group_button_locator).get_attribute('class')

            def click_delete_group(self):
                self.find_element(*self._delete_group_button_locator).click()
                from pages.groups_page import GroupsPage
                return GroupsPage(self.page.selenium, self.page.base_url)

    class AccessTab(Region):
        _group_type_form_locator = (By.ID, 'grouptype-form')

        @property
        def group_type(self):
            return self.GroupTypeForm(self.page, self.find_element(*self._group_type_form_locator))

        class GroupTypeForm(Region):
            _reviewed_type_locator = (By.ID, 'id_accepting_new_members_1')
            _new_member_criteria_locator = (By.ID, 'id_new_member_criteria_fieldset')

            def set_reviewed_group_type(self):
                self.find_element(*self._reviewed_type_locator).click()

            @property
            def is_member_criteria_visible(self):
                return self.find_element(*self._new_member_criteria_locator).is_displayed()

    class InvitationsTab(Region):
        _invite_form_locator = (By.ID, 'invite-form')
        _invitations_list_form_locator = (By.ID, 'invitations-form')

        @property
        def invitations_list(self):
            return self.InvitationsForm(self.page, self.find_element(*self._invitations_list_form_locator))

        @property
        def invite(self):
            return self.InviteForm(self.page, self.find_element(*self._invite_form_locator))

        class InvitationsForm(Region):
            _invitatation_list_locator = (By.CSS_SELECTOR, '.invitee')

            @property
            def search_invitation_list(self):
                return [self.SearchResult(self.page, el) for el in
                        self.find_elements(*self._invitatation_list_locator)]

            class SearchResult(Region):
                _name_locator = (By.CSS_SELECTOR, '.invitee a:nth-child(2)')

                @property
                def name(self):
                    return self.find_element(*self._name_locator).text

        class InviteForm(Region):
            _invite_search_locator = (By.CSS_SELECTOR, '.select2-search__field')
            _invite_locator = (By.ID, 'form-submit-invite')

            def invite_new_member(self, mozillian):
                search = self.find_element(*self._invite_search_locator)
                search.send_keys(mozillian)
                self.wait.until(expected.visibility_of_element_located((
                    By.XPATH, '//li[contains(text(), "{0}")]'.format(mozillian)))).click()

            def click_invite(self):
                self.find_element(*self._invite_locator).click()
