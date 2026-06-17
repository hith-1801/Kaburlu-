from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Button
from textual.containers import Container, Vertical
from textual.screen import Screen

class InputScreen(Screen):
    """Screen for collecting user inputs"""
    def __init__(self):
        super().__init__()
        self.inputs = ["hostname", "nickname", "channel", "port"]
        self.ident = 0
        self.actually = {}

    CSS = """
    Screen {
        layout: horizontal;    
        align: center middle;
    }
    #panel1 {
        width: 50%;
        height: 50%;
        background: #333333;
        color: white;
        border: solid #666666;
        padding: 2;
    }
    #panel2 {
        width: 50%;
        height: 50%;
        background: #000000;
        color: white;
        border: solid white;
        padding: 2;
    }
    #input-field {
        width: 80%; 
        margin: 1 0;
    }
    #prompt {
        margin-bottom: 1;
        text-align: center;
    }
    #prompt1 {
        margin-bottom: 1;
        text-align: center;
    }
    """

    def compose(self) -> ComposeResult:
        with Container(id="panel1"):
            yield Static(f"Enter {self.inputs[self.ident]}", id="prompt")
            yield Input(placeholder=f"Type {self.inputs[self.ident]} here...", 
                       id="input-field", classes="input-field")
        with Container(id="panel2"):
            yield Static("Input details will appear here", id="prompt1")

    def on_mount(self):
        self.query_one("#input-field").focus()

    def on_input_submitted(self, event: Input.Submitted):
        value = event.value.strip()
        
        if value:
            # Store the current input
            current_field = self.inputs[self.ident]
            self.actually[current_field] = value
            
            # Update the display panel
            display_text = "\n".join([f"{k}: {v}" for k, v in self.actually.items()])
            self.query_one("#prompt1").update(display_text)
            
            # Move to next input or finish
            self.ident += 1
            
            if self.ident < len(self.inputs):
                # Update for next input
                self.query_one("#prompt").update(f"Enter {self.inputs[self.ident]}")
                input_field = self.query_one("#input-field")
                input_field.value = ""
                input_field.placeholder = f"Type {self.inputs[self.ident]} here..."
            else:
                # All inputs collected, switch to chat screen
                self.app.switch_to_chat(self.actually)
        else:
            self.query_one("#prompt").update(f"Please enter {self.inputs[self.ident]}!")


class ChatScreen(Screen):
    """Screen for displaying chat interface"""
    
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data or {}
        self.chat_messages = []  # Store chat messages

    CSS = """
    Screen {
        layout: vertical;    
    }
    #panel3 {
        width: 100%;
        height: 80%;
        background: #333333;
        color: white;
        border: solid #666666;
        padding: 2;
        overflow-y: auto;
    }
    #panel4 {
        width: 100%;
        height: 20%;
        background: #000000;
        color: white;
        border: solid white;
        padding: 2;
    }
    #input-container {
        layout: horizontal;
        width: 100%;
    }
    #message-input {
        width: 80%;
        margin-right: 1;
    }
    #send-btn {
        width: 20%;
    }
    """

    def compose(self) -> ComposeResult:
        # Display panel for chat messages
        yield Static(self.format_user_data(), id="panel3")
        
        # Input panel at bottom with message input
        with Container(id="panel4"):
            with Container(id="input-container"):
                yield Input(placeholder="Type your message...", id="message-input")
                yield Button("Send", id="send-btn")

    def on_mount(self):
        # Focus on message input when screen mounts
        self.query_one("#message-input").focus()

    def format_user_data(self):
        """Format the user data for display"""
        if not self.user_data:
            return "No data available"
        return "\n".join([f"{key}: {value}" for key, value in self.user_data.items()])

    def update_display(self, new_message=None):
        """Update the display panel with messages"""
        if new_message:
            self.chat_messages.append(new_message)
        
        # Combine user data and chat messages
        output = self.format_user_data()
        if self.chat_messages:
            output += "\n\n" + "\n".join(self.chat_messages)
        
        self.query_one("#panel3").update(output)

    def on_button_pressed(self, event):
        """Handle send button click"""
        if event.button.id == "send-btn":
            self.send_message()

    def on_input_submitted(self, event):
        """Handle ENTER key in message input"""
        if event.input.id == "message-input":
            self.send_message()

    def send_message(self):
        """Send a message from the input field"""
        input_field = self.query_one("#message-input")
        message = input_field.value.strip()
        
        if message:
            self.update_display(f"Message: {message}")
            input_field.value = ""
            self.query_one("#panel3").scroll_end()


class MainApp(App):
    """Main application that manages both screens"""
    CSS = """
    /* Global styles can go here */
    """
    
    def __init__(self):
        super().__init__()
        self.user_data = {}
        # Install screens for the app's lifetime
        self.install_screen(InputScreen(), "input")
        self.install_screen(ChatScreen(), "chat")  # Initialize with empty data

    def on_mount(self):
        # Start with the input screen
        self.push_screen("input")

    def switch_to_chat(self, user_data):
        """Switch to chat screen with the collected data"""
        self.user_data = user_data
        # Get the chat screen and update its data
        chat_screen = self.get_screen("chat")
        chat_screen.user_data = user_data
        
        # Wait for the screen to mount before updating
        # The update will happen in the screen's on_mount
        self.switch_screen("chat")
        
        # Update the display after switch (when widgets are rendered)
        self.call_after_refresh(chat_screen.update_display)


if __name__ == "__main__":
    app = MainApp()
    result = app.run()
    print("Application finished")