import QtQuick 1.0
import org.kde.plasma.components 0.1 as PlasmaComponents
import org.kde.plasma.core 0.1 as PlasmaCore

Item {
    id: main
    width: 48
    height: 48
    property int     minimumWidth: 48
    property int     minimumHeight: 48
    property int     interval: plasmoid.readConfig("interval")
    property string  normalColor: plasmoid.readConfig("normal_color")
    property string  overheatColor: plasmoid.readConfig("overheat_color")
    property string  overheatLevel: plasmoid.readConfig("overheat_level")
    property string  units: plasmoid.readConfig("units")
    property string  sensor: plasmoid.readConfig("sensor")
    property string  font: plasmoid.readConfig("font")
    property string  fontFamily: font.toString().split(',')[0]
    property string  fontSize: font.toString().split(',')[1]
    
    PlasmaCore.Theme {
        id: theme
    }
    
    Component.onCompleted: {
        plasmoid.addEventListener('ConfigChanged', function () {
            print(plasmoid.readConfig('font'))
            
            plasmoid.activeConfig = "main";
            font = plasmoid.readConfig('font')
            interval = plasmoid.readConfig('interval')
            normalColor = plasmoid.readConfig('normalColor')
            overheatColor = plasmoid.readConfig('overheatColor')
            overheatLevel = plasmoid.readConfig('overheatLevel')
            units = plasmoid.readConfig('units')
            sensor = plasmoid.readConfig('sensor')
            
            text.color = normalColor
            
        })
    }
    
    Text {
        id: text
        color: normalColor
        visible: true
        text: i18n("10 C")
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        font {
            family: fontFamily
            pointSize: fontSize
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