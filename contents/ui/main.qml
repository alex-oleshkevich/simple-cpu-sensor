import QtQuick 1.1
import org.kde.plasma.core 0.1 as PlasmaCore
import org.kde.plasma.components 0.1 as Components

Item {
    id: main
      
    property int     interval
    property string  normalColor
    property string  overheatColor
    property int     overheatLevel
    property string  fontFamily
    property bool    fontBold
    property bool    fontItalic
    property int     fontSize
    property int     usedUnits
    property bool    displayUnitsSign: true
    property string  label: 'N/A'
    property string  labelColor: normalColor
    property bool    isSourceRegistered: false
    
    Text {
        id: textLabel
        text: label
        color: labelColor
        font {
            family: fontFamily
            pixelSize: fontSize
            bold: fontBold
            italic: fontItalic
        }
        wrapMode: Text.NoWrap
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        anchors {
            centerIn: parent
            left: parent.left
            right: parent.right
        }
        
    }
    
    Component.onCompleted: {
        plasmoid.addEventListener('ConfigChanged', function () {
            fontFamily = plasmoid.readConfig('font')
            fontSize = plasmoid.readConfig('fontSize')
            fontBold = plasmoid.readConfig('fontBold')
            fontItalic = plasmoid.readConfig('fontItalic')
            interval = plasmoid.readConfig('interval')
            normalColor = plasmoid.readConfig('normalColor')
            overheatColor = plasmoid.readConfig('overheatColor')
            overheatLevel = plasmoid.readConfig('overheatLevel')
            
            usedUnits = plasmoid.readConfig('units')
            displayUnitsSign = plasmoid.readConfig('displayUnitsSign')
            
            tooltip.mainText = 'Confing completed'
        })
    }
    
    PlasmaCore.DataSource {
        id: temperatureDataSource
        engine: "systemmonitor"
        interval: main.interval
        connectedSources: detectSource(sources)
        onNewData: {
            setTemperatureValue(data.value)
        }
    }
    
    function detectSource(sources) {
        if (isSourceRegistered) {
            return temperatureDataSource.connectedSources
        }
        
        var detected = []
        for (var i in sources) {
            var source = sources[i]
            if (source.match(/lmsensors\/(k\d+temp|coretemp)/)) {
                isSourceRegistered = true
                detected.push(source)
                print('Source registered: ' + source)
                break
            }
        }
        return detected
    }
    
    function setTemperatureValue(value) {
        if (value) {
            var value = Math.ceil(value)
            if (value > overheatLevel) {
                labelColor = overheatColor
            } else {
                labelColor = normalColor
            }

           label = formatValue(value)
        } else {
            label = 'ERR'
        }
    }
    
    function formatValue(value) {
        var symbol  = 'C'
        switch (usedUnits) {
            case 0:
            default:
                symbol = 'C'
                break
            case 1:
                value = Math.ceil(value * 9/5.0 + 32)
                symbol = 'F'
                break
        }
        
        if (displayUnitsSign == false) {
            symbol = '';
        }
        
        return value + '°' + symbol
    }
}