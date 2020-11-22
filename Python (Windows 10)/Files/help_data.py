# Data for Help Window


# General Usage Node Data (general_usage_node)
general_usage_node_data = {"How to connect to database?": {
                                                       "name": "How to connect to database?",
                                                       "type": "General Connection",
                                                       "children": None,
                                                       "description": """\
You can connect to a MySQL database by:

1. Setting up and starting your web server with a database.
2. Fill in required security and login details for your database connection.
3. Go to Main window and go to Connection > Connect to Database.
4. You have connected to your MySQL web database!


INFO: Make sure you enter correct details for your database and save new changes!\
"""
                                                      },
                              "What is the default port?": {
                                                       "name": "What is the default port?",
                                                       "type": "General Connection",
                                                       "children": None,
                                                       "description": "Default port for MySQL connections is 3306."
                              }
}

# Settings Keybinds Node Data (settings_keybinds_node)
settings_keybinds_node_data = {"Quick Save": {
                                          "name": "Quick Save (CTRL-S)",
                                          "type": "Settings Keybinds and Shortcuts",
                                          "children": None,
                                          "description": "You can use (CTRL-S) to quick save on a settings window!"
                                          },
                               "Test Connection": {
                                          "name": "Test Connection (CTRL-P)",
                                          "type": "Settings Keybinds and Shortcuts",
                                          "children": None,
                                          "description": "You can use (CTRL-P) to quick save on a settings window!"
                                          },
                              "Go Back": {
                                          "name": "Go Back (CTRL-B)",
                                          "type": "Settings Keybinds and Shortcuts",
                                          "children": None,
                                          "description": "You can use (CTRL-B) to go back to main menu from a settings window!"
                                          }
}

# Usage Node Data (usage_node)
usage_node_data = {"General": {
                           "name": "General",
                           "type": "General Usage Help",
                           "children": general_usage_node_data,
                           "description": "General Usage help and information to be used across the software."
                            }
}

# Keybinds Node Data (keybinds_node)
keybinds_node_data = {"Settings": {
                               "name": "Settings",
                               "type": "Keybinds for Settings",
                               "children": None,
                               "description": "Keybind/Shortcut information and help for Settings window."
                              }
}


# Main Node Data (main_node)
main_node_data = {"Usage": {
                        "name": "Usage",
                        "type": "Help Type",
                        "children": usage_node_data,
                        "description": "Help related to the Usage of the software."
                        },
                  "Keybinds": {
                        "name": "Keybinds",
                        "type": "Help Type",
                        "children": keybinds_node_data,
                        "description": "Help related to Keybinds and Shortcuts on the software."
                        }
}