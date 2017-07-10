# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base import Base
from pages.page import PageRegion


class EditGroupPage(Base):
    _description_button_locator = (By.ID, 'description-tab')
    _description_tab_locator = (By.ID, 'description')
    _access_button_locator = (By.ID, 'access-tab')
    _access_tab_locator = (By.ID, 'access')
    _invitations_button_locator = (By.ID, 'invitations-tab')
    _invitations_tab_locator = (By.ID, 'invitations')

    def __init__(self, base_url, selenium):
        super(EditGroupPage, self).__init__(base_url, selenium)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_element_visible(*self._description_button_locator))

    @property
    def description(self):
        self.selenium.find_element(*self._description_button_locator).click()
        return self.DescriptionTab(self.base_url, self.selenium,
                                   self.selenium.find_element(*self._description_tab_locator))

    @property
    def access(self):
        self.selenium.find_element(*self._access_button_locator).click()
        return self.AccessTab(self.base_url, self.selenium,
                              self.selenium.find_element(*self._access_tab_locator))

    @property
    def invitations(self):
        self.wait_for_element_visible(*self._invitations_button_locator)
        self.selenium.find_element(*self._invitations_button_locator).click()
        return self.InvitationsTab(self.base_url, self.selenium,
                                   self.selenium.find_element(*self._invitations_tab_locator))

    class DescriptionTab(PageRegion):
        _description_form_locator = (By.ID, 'description-form')
        _delete_panel_locator = (By.CSS_SELECTOR, '.panel-danger')

        @property
        def description_info(self):
            return self.DescriptionForm(self.base_url, self.selenium,
                                        self._root_element.find_element(*self._description_form_locator))

        @property
        def delete_group(self):
            return self.DeletePanel(self.base_url, self.selenium,
                                    self._root_element.find_element(*self._delete_panel_locator))

        class DescriptionForm(PageRegion):
            _description_locator = (By.ID, 'id_description')
            _irc_channel_locator = (By.ID, 'id_irc_channel')
            _update_locator = (By.ID, 'form-submit-description')

            def set_description(self, description_text):
                element = self._root_element.find_element(*self._description_locator)
                element.clear()
                element.send_keys(description_text)

            def set_irc_channel(self, irc_channel):
                element = self._root_element.find_element(*self._irc_channel_locator)
                element.clear()
                element.send_keys(irc_channel)

            def click_update(self):
                self._root_element.find_element(*self._update_locator).click()
                self.wait_for_element_not_present(*self._update_locator)
                self.wait_for_element_present(*self._update_locator)

        class DeletePanel(PageRegion):
            _delete_acknowledgement_locator = (By.ID, 'delete-checkbox')
            _delete_group_button_locator = (By.ID, 'delete-group')

            def check_acknowledgement(self):
                self._root_element.find_element(*self._delete_acknowledgement_locator).click()

            @property
            def is_delete_button_enabled(self):
                return 'disabled' not in self._root_element.find_element(*self._delete_group_button_locator).get_attribute('class')

            def click_delete_group(self):
                self._root_element.find_element(*self._delete_group_button_locator).click()
                from pages.groups_page import GroupsPage
                return GroupsPage(self.base_url, self.selenium)

    class AccessTab(PageRegion):
        _group_type_form_locator = (By.ID, 'grouptype-form')

        @property
        def group_type(self):
            return self.GroupTypeForm(self.base_url, self.selenium,
                                      self._root_element.find_element(*self._group_type_form_locator))

        class GroupTypeForm(PageRegion):
            _reviewed_type_locator = (By.ID, 'id_accepting_new_members_1')
            _new_member_criteria_locator = (By.ID, 'id_new_member_criteria_fieldset')

            def set_reviewed_group_type(self):
                self._root_element.find_element(*self._reviewed_type_locator).click()

            @property
            def is_member_criteria_visible(self):
                return self._root_element.find_element(*self._new_member_criteria_locator).is_displayed()

    class InvitationsTab(PageRegion):
        _invite_form_locator = (By.ID, 'invite-form')
        _invitations_list_form_locator = (By.ID, 'invitations-form')

        @property
        def invitations_list(self):
            return self.InvitationsForm(self.base_url, self.selenium,
                                        self._root_element.find_element(*self._invitations_list_form_locator))

        @property
        def invite(self):
            return self.InviteForm(self.base_url, self.selenium,
                                   self._root_element.find_element(*self._invite_form_locator))

        class InvitationsForm(PageRegion):
            _invitatation_list_locator = (By.CSS_SELECTOR, '.invitee')

            @property
            def search_invitation_list(self):
                return [self.SearchResult(self.base_url, self.selenium, el) for el in
                        self.selenium.find_elements(*self._invitatation_list_locator)]

            class SearchResult(PageRegion):
                _name_locator = (By.CSS_SELECTOR, '.invitee a:nth-child(2)')

                @property
                def name(self):
                    return self._root_element.find_element(*self._name_locator).text

        class InviteForm(PageRegion):
            _invite_search_locator = (By.CSS_SELECTOR, '.select2-search__field')
            _invite_locator = (By.ID, 'form-submit-invite')

            def invite_new_member(self, mozillian):
                search = self._root_element.find_element(*self._invite_search_locator)
                search.send_keys(mozillian)
                self.wait_for_element_visible(By.XPATH, '//li[contains(text(), "{0}")]'.format(mozillian))
                result = self._root_element.find_element(By.XPATH, '//li[contains(text(), "{0}")]'.format(mozillian))
                result.click()

            def click_invite(self):
                self._root_element.find_element(*self._invite_locator).click()
