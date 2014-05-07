import QtQuick 1.0
import org.kde.plasma.components 0.1 as PlasmaComponents
import org.kde.plasma.core 0.1 as PlasmaCore

Item {
    id: main
    width: 300
    height: 300
    property variant build: {}
    property int     interval: plasmoid.readConfig("interval")
    property string  host: plasmoid.readConfig("host")
    property string  username: plasmoid.readConfig("username")
    property string  password: plasmoid.readConfig("password")
    property string  plan: plasmoid.readConfig("plan")
    property bool    isConfigured: false
    
    PlasmaCore.Theme {
        id: theme
    }
    
    PlasmaComponents.Label {
        id: display
        visible: true
        text: i18n("10 C")
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        font: {
            family: theme.family
            pointSize: theme.defaultFont.pointSize
        }
    }
    
    PlasmaCore.DataSource {
            id: dataSource
            engine: "systemmonitor"
            connectedSources: ["Local","UTC"]
            interval: 500

            onNewData: {
                console.log(data)
            }

    }
}