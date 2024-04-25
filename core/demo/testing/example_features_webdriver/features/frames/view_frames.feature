Feature: View Frames
  View frames are a way to view the contents of a frame in a separate window. This is useful when you want to see the contents of a frame without having to switch to it. You can view the contents of a frame by selecting the frame in the Frames view and clicking the View Frame button. This will open a new window that displays the contents of the frame. You can then interact with the frame in the same way as you would in the main window, including editing the contents of the frame.

Scenario Outline:
  Given I am on the frames page
  When I select a frame with type "<frame type>"
  Then the frame loads successfully

Examples:
  | frame type    |
  | i_frame       |
  | nested_frame  |