//! [import]
import QtQuick
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.4
import QtQuick.Controls.Universal 2.4
import QtCharts 2.2
import QtQuick3D
//! [import]

ApplicationWindow {
    id: window
    width: 200
    height: 200
    visible: true

    //![Init Menu Bar]
    menuBar: MenuBar {
      Menu {
        title: '&File'
        Action { text: '&New...' }
        Action { text: '&Open...' }
        Action { text: '&Save' }
        Action { text: 'Save &As...' }
        MenuSeparator {}
        Action { text: '&Quit' }
      }
      Menu {
         title: '&Edit'
         Action { text: 'Cu&t' }
         Action { text: '&Copy' }
         Action { text: '&Paste' }
       }
       Menu {
         title: '&Help'
         Action { text: '&About' }
       }
    }
    //![End Menu Bar]

    Pane {
      padding: 10
      anchors.fill: parent
      GridLayout {
        anchors.fill: parent
        flow: GridLayout.TopToBottom
        rows: 2
        CellBox {
          title: 'Buttons'
          ColumnLayout {
            anchors.fill: parent
            Button {
              text: 'Button'
              Layout.fillWidth: true
              onClicked: normalPopup.open()
            }
            Button {
              text: 'Flat'
              Layout.fillWidth: true
              flat: true
              onClicked: modalPopup.open()
            }
            Button {
              text: 'Highlighted'
              Layout.fillWidth: true
              highlighted: true
              onClicked: dialog.open()
            }
            RoundButton {
              text: '+'
              Layout.alignment: Qt.AlignHCenter
            }
          }
        }
        CellBox {
          title: 'Radio Buttons'
          ColumnLayout {
            anchors.fill: parent
            RadioButton { text: 'Radio Button 1'; checked: true }
            RadioButton { text: 'Radio Button 2' }
            RadioButton { text: 'Radio Button 3' }
            RadioButton { text: 'Radio Button 4' }
          }
        }
        CellBox {
          title: 'Check Boxes'
          ColumnLayout {
            anchors.fill: parent
            Switch { Layout.alignment: Qt.AlignHCenter }
            ButtonGroup {
              id: childGroup
              exclusive: false
              checkState: parentBox.checkState
            }
            CheckBox {
              id: parentBox
              text: 'Parent'
              checkState: childGroup.checkState
            }
            CheckBox {
              checked: true
              text: 'Child 1'
              leftPadding: indicator.width
              ButtonGroup.group: childGroup
            }
            CheckBox {
              text: 'Child 2'
              leftPadding: indicator.width
              ButtonGroup.group: childGroup
            }
          }
        }
        CellBox {
          title: 'Progress Indicators'
          ColumnLayout {
            anchors.fill: parent
            BusyIndicator {
              running: true
              Layout.alignment: Qt.AlignHCenter
              ToolTip.visible: hovered
              ToolTip.text: 'Busy Indicator'
            }
            DelayButton {
              text: 'Delay Button'
              delay: 3000
              Layout.fillWidth: true
            }
            ProgressBar { value: 0.6; Layout.fillWidth: true }
            ProgressBar { indeterminate: true; Layout.fillWidth: true }
          }
        }
        CellBox {
            title: 'ComboBoxes'
            ColumnLayout {
                anchors.fill: parent
                ComboBox {
                  model: ['Normal', 'Second', 'Third']
                  Layout.fillWidth: true
                }
                ComboBox {
                  model: ['Flat', 'Second', 'Third']
                  Layout.fillWidth: true
                  flat: true
                }
                ComboBox {
                  model: ['Editable', 'Second', 'Third']
                  Layout.fillWidth: true
                  editable: true
                }
                ComboBox {
                    model: 10
                    editable: true
                    validator: IntValidator { top: 9; bottom: 0 }
                    Layout.fillWidth: true
                }
            }
        }
        CellBox {
          title: 'Range Controllers'
          ColumnLayout {
            anchors.fill: parent
            Dial {
              id: dial
              scale: 0.8
              Layout.alignment: Qt.AlignHCenter
              ToolTip {
                parent: dial.handle
                visible: dial.pressed
                text: dial.value.toFixed(2)
              }
            }
            RangeSlider {
              first.value: 0.25; second.value: 0.75; Layout.fillWidth: true
              ToolTip.visible: hovered
              ToolTip.text: 'Range Slider'
            }
            Slider {
              id: slider
              Layout.fillWidth: true
              ToolTip {
                parent: slider.handle
                visible: slider.pressed
                text: slider.value.toFixed(2)
              }
            }
          }
        }
        CellBox {
          Layout.rowSpan: 2; Layout.minimumWidth: 700
          title: 'Tabs'
          Layout.preferredWidth: height // Keep the ratio right!
          StackLayout {
            width: parent.width - x
            height: parent.height - y
            View3D {
                id: view
                width: parent.width - x
                height: parent.height - y

                //! [environment]
                environment: SceneEnvironment {
                    clearColor: "skyblue"
                    backgroundMode: SceneEnvironment.Color
                }
                //! [environment]

                //! [camera]
                PerspectiveCamera {
                    position: Qt.vector3d(0, 200, 300)
                    eulerRotation.x: -30
                }
                //! [camera]

                //! [light]
                DirectionalLight {
                    eulerRotation.x: -30
                    eulerRotation.y: -70
                }
                //! [light]

                //! [objects]
                Model {
                    position: Qt.vector3d(0, -200, 0)
                    source: "#Cylinder"
                    scale: Qt.vector3d(2, 0.2, 1)
                    materials: [ DefaultMaterial {
                            diffuseColor: "red"
                            indexOfRefraction: 1.0
                            opacity: 0.1
                        }
                    ]
                }

                Model {
                    position: Qt.vector3d(0, -200, 0)
                    source: "#Cylinder"
                    scale: Qt.vector3d(1.5, 0.2, 1)

                    materials: [ DefaultMaterial {
                            diffuseColor: "blue"
                        }
                    ]
                }

                //! [objects]
            }
          }
        }
        Popup {
          id: normalPopup
          ColumnLayout {
            anchors.fill: parent
            Label { text: 'Normal Popup' }
            CheckBox { text: 'E-mail' }
            CheckBox { text: 'Calendar' }
            CheckBox { text: 'Contacts' }
          }
        }
        Popup {
          id: modalPopup
          modal: true
          ColumnLayout {
            anchors.fill: parent
            Label { text: 'Modal Popup' }
            CheckBox { text: 'E-mail' }
            CheckBox { text: 'Calendar' }
            CheckBox { text: 'Contacts' }
          }
        }
        Dialog {
          id: dialog
          title: 'Dialog'
          Label { text: 'The standard dialog.' }
          footer: DialogButtonBox {
            standardButtons: DialogButtonBox.Ok | DialogButtonBox.Cancel
          }
        }
      }
    }


}
