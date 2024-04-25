Feature: View Status Codes
  View status codes for different pages.

Scenario Outline:
  Given I am on the status page
  When I select with type "<frame type>" status
  Then the page for the status is loaded successfully

Examples:
  | status  |
  | 200     |
  | 301     |
  | 404     |
  | 500     |