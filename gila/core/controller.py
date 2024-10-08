from PySide6.QtCore import QObject, Signal, Slot


class Controller(QObject):
    user_prompt_to_model = Signal(str)
    response_message_to_chatlog = Signal(str)
    response_info_to_chatlog = Signal(dict)
    new_settings_to_manager = Signal(str, float, int)
    new_chat_started_to_model = Signal()
    update_status_bar = Signal(str)
    missing_api_key_to_view = Signal(str)
    api_key_to_manager = Signal(str, str)
    api_key_is_valid_to_view = Signal(bool)
    loading_saved_chat_id_to_manager = Signal(str)

    def __init__(self, model, view, thread):
        super().__init__()
        self.model = model
        self.view = view
        self.main_thread = thread
        self.connect_model()
        self.connect_view()
        # self.model.check_for_updates()

    def connect_model(self):
        # Connect CONTROLLER's signals to MODEL's slots
        self.user_prompt_to_model.connect(self.model.get_user_prompt_slot)
        self.new_settings_to_manager.connect(
            self.model.manager.set_new_settings_slot)
        self.api_key_to_manager.connect(self.model.manager.api_key_slot)
        self.loading_saved_chat_id_to_manager.connect(self.model.manager.restore_chat_from_id_slot)

        # Connect MODEL's signals to CONTROLLER's slots
        self.model.response_message_signal_to_controller.connect(
            self.response_message_slot)
        self.model.response_info_signal_to_controller.connect(
            self.response_info_slot)
        self.model.start_new_chat_to_controller.connect(
            self.new_chat_started_slot)
        self.model.connection_error_to_controller.connect(
            self.connection_error_slot)
        self.model.generic_error_to_controller.connect(
            self.generic_error_slot)
        self.model.update_found_to_controller.connect(
            self.update_found_slot)
        self.model.manager.api_key_is_valid_to_controller.connect(
            self.api_key_is_valid_slot)

    def connect_view(self):
        # Connect CONTROLLER's signals to VIEW's slots
        self.response_message_to_chatlog.connect(
            self.view.chat.get_response_message_slot)
        self.response_info_to_chatlog.connect(
            self.view.chat.get_response_info_slot)
        self.update_status_bar.connect(
            self.view.status_bar.on_status_update_slot)
        self.missing_api_key_to_view.connect(
            self.view.add_api_key_modal_slot)
        self.api_key_is_valid_to_view.connect(
            self.view.add_api_key_modal.on_api_key_validation_slot)

        # Connect VIEW's signals to CONTROLLER's slots
        self.view.window_closed_signal_to_controller.connect(
            self.window_was_closed_slot)
        self.view.sidebar.change_settings_modal.new_settings_to_controller.connect(
            self.new_settings_to_manager)
        self.view.sidebar.stop_chat_to_controller.connect(
            self.chat_stopped_from_sidebar_slot)
        self.view.sidebar.stored_chats.loading_saved_chat_id_to_controller.connect(
            self.loading_saved_chat_id_slot)
        self.view.chat.user_prompt_signal_to_controller.connect(
            self.user_prompt_slot)
        self.view.chat.start_new_chat_to_controller.connect(
            self.new_chat_started_slot)
        self.view.add_api_key_modal.api_key_to_controller.connect(
            self.api_key_from_modal_slot)

        # Connect ChatLog to Status Bar
        self.view.chat.update_status_bar_from_chatlog.connect(
            self.view.status_bar.on_status_update_slot)

    @Slot()
    def update_found_slot(self):
        self.update_status_bar.emit("Update found.")
        self.view.update_found_modal.exec_()

    @Slot(str)
    def response_message_slot(self, response_message):
        """ Slot
        Connected to one signal:
            - model.response_message_signal_to_controller
        Emits two signals:
            - response_message_to_chatlog (view.chat.get_response_message_slot)
            - update_status_bar (view.status_bar.on_status_update_slot)

        Receive AI response from the MODEL and send it to CHATLOG
        """
        self.response_message_to_chatlog.emit(response_message)
        self.update_status_bar.emit(
            "Response received. Waiting for a new message...")

    @Slot(dict)
    def response_info_slot(self, response_info):
        """ Slot
        Connected to one signal:
            - model.response_info_signal_to_controller
        Emits two signals:
            - response_info_to_chatlog (view.chat.get_response_message_slot)

        Receive response info from the MODEL and send it to SIDEBAR
        """
        self.response_info_to_chatlog.emit(response_info)

    @Slot(str)
    def user_prompt_slot(self, user_prompt):
        """ Slot
        Connected to one signal:
            - view.chat.user_prompt_signal_to_controller
        Emits two signals:
            - user_prompt_to_model (model.get_user_prompt_slot)
            - update_status_bar (view.status_bar.on_status_update_slot)
        """
        self.user_prompt_to_model.emit(user_prompt)
        self.update_status_bar.emit("I'm sending the message...")

    @Slot(str, float, int)
    def settings_changed_from_sidebar_slot(self, new_client, new_temperature, new_max_tokens):
        """ Slot
        Connected to new settings sidebar signal
            - view.sidebar.new_settings_to_controller
        Emits two signals:
            - new_settings_to_manager (model.manager.set_new_client_slot)
            - update_status_bar (view.status_bar.on_status_update_slot)
        """
        self.new_settings_to_manager.emit(new_client, new_temperature, new_max_tokens)
        self.update_status_bar.emit(f"You have selected {new_client} with {new_temperature} temperature.")

    @Slot()
    def chat_stopped_from_sidebar_slot(self):
        """ Slot
        Connected to stopping signal from Sidebar:
            - view.sidebar.stop_chat_to_controller
        Saves current chat, cleans log, resets chat and emits two signals:
            - chat_stopped_to_model (model.chat_stopped_slot)
            - update_status_bar (view.status_bar.on_status_update_slot)
        """
        if self.model.manager.stream_stopped is not True:
            # Chat must be saved only if it's not empty and date must not be changed if chatlog is not changed
            if self.view.chat.chatlog_has_changed(self.model.manager.client.chat_id) and self.view.chat.chatlog_has_text():
                self.model.manager.save_current_chat()
                # Adds a new saved_chat_button passing chat_id as argument
                self.view.sidebar.stored_chats.add_stored_chat_button(self.model.manager.client.chat_id)
                self.view.chat.add_log_to_saved_chat_data(self.model.manager.client.chat_id)
            self.main_thread.stop()
            self.view.chat.log_widget.clear()
            self.model.client.on_chat_reset()
            self.model.manager.stream_stopped = True
            self.update_status_bar.emit("The conversation has been closed.")

    @Slot()
    def new_chat_started_slot(self):
        """ Slot
        Connected to two signals:
            - view.chat.start_new_chat_to_controller
            - model.start_new_chat_to_controller
        Checks API Key and emits two signals:
            - update_status_bar (view.status_bar.on_status_update_slot)
            - missing_api_key_to_view (view.add_api_key_modal_slot)
        """
        # Check if manager has changed the client: if so, update setting accordingly
        if self.model.manager.next_client:
            self.model.manager.client = self.model.manager.next_client[0]
            self.model.manager.client.llm_name = self.model.manager.next_client[1]
            self.model.manager.client.temperature = self.model.manager.next_temperature
            self.model.manager.client.max_tokens = self.model.manager.next_max_tokens
            self.model.manager.client.on_chat_reset()
            self.model.manager.next_client = None
        # Update settings label on the sidebar
        self.view.sidebar.current_settings.update_settings_label(
            self.model.manager.on_current_settings())
        self.view.sidebar.change_settings_modal.update_current_settings(
            self.model.manager.on_current_settings())
        self.model.manager.update_saved_settings()
        self.view.chat.update_chat_title()
        self.view.chat.on_response_info_labels_reset()
        self.view.sidebar.stored_chats.current_chat_id = self.model.manager.client.chat_id
        # If there is connection, start a new conversation
        if self.model.manager.check_internet_connection():
            self.model.manager.stream_stopped = False
            self.update_status_bar.emit("New conversation started.")
            # Check if API Key is valid. if it is, show chatlog and run the thread
            if self.model.manager.on_api_key() is False:
                self.missing_api_key_to_view.emit(self.model.manager.client.company)
            else:
                self.view.on_show_chatlog_and_prompt_line()
                self.view.sidebar.current_settings.on_show_widgets()
                self.view.sidebar.on_show_widgets()
            self.model.running = True
            self.main_thread.model.run()
            return
        # Open a modal that warns user about the lack of connection
        self.update_status_bar.emit("No internet connection.")
        self.view.on_hide_chatlog_and_prompt_line()
        self.view.warning_modal.on_no_internet_connection_label()
        self.view.warning_modal.exec_()

    @Slot(str, str)
    def api_key_from_modal_slot(self, api_key, company_name):
        """ Slot
        Connected to one signal:
            - view.modal.api_key_to_controller
        Emits one signal:
            - api_key_to_manager (model.manager.api_key_slot)
        If company_name parameter is set by AddAPIKeyModal via process_api_key
        method. If it is None, manager will send new API key to the current client,
        else it will send it on the client based on that company name.
        """
        self.api_key_to_manager.emit(api_key, company_name)

    @Slot(bool)
    def api_key_is_valid_slot(self, is_key_valid):
        """ Slot
        Connected to one signal:
            - model.manager.api_key_is_valid_to_controller
        Emits one signal:
            - api_key_is_valid_to_view (view.modal.on_api_key_validation_slot)
        """
        self.api_key_is_valid_to_view.emit(is_key_valid)

    @Slot()
    def connection_error_slot(self):
        """ Slot
        Connected to one signal:
            - model.connection_error_to_controller
        Opens WarningLabel to warn user about internet connection.
        """
        self.response_message_to_chatlog.emit("<span style='color:#f00'>Nessuna connessione a internet!</span>")
        self.update_status_bar.emit("Nessuna connessione a internet.")
        self.view.warning_modal.on_no_internet_connection_label()
        self.view.warning_modal.exec_()

    @Slot(str)
    def generic_error_slot(self, error):
        """ Slot
        Connected to one signal:
            - model.generic_error_to_controller
        Opens WarningLabel to warn user about internet connection.
        """
        self.response_message_to_chatlog.emit("<span style='color:#f00'>An error has occurred! Try again!</span>")
        self.update_status_bar.emit("An error has occurred.")
        self.view.warning_modal.on_label(error)
        self.view.warning_modal.exec_()

    @Slot(str)
    def loading_saved_chat_id_slot(self, chat_id):
        """ Slot
        Connected to one signal:
            - view.sidebar.stored_chats.loading_saved_chat_id_to_controller
        Sends chat_id to manager
        """
        self.chat_stopped_from_sidebar_slot()
        self.loading_saved_chat_id_to_manager.emit(chat_id)
        self.view.chat.log_widget.append(self.view.sidebar.stored_chats.chatlog)
        self.new_chat_started_slot()

    @Slot()
    def window_was_closed_slot(self):
        """ Slot
        Connected to one signal:
        """
        if self.view.chat.chatlog_has_text():
            self.model.manager.save_current_chat()
            self.view.chat.add_log_to_saved_chat_data(self.model.manager.client.chat_id)
        if self.model.running:
            self.main_thread.stop()
            self.model.running = False
