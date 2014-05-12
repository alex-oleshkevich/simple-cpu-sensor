import QtQuick 1.1
import org.kde.plasma.core 0.1 as PlasmaCore
import org.kde.plasma.components 0.1 as Components

Item {
    id: main
      
    property int     interval: 1000
    property string  normalColor: theme.textColor
    property string  overheatColor: '#f00'
    property int     overheatLevel: 80
    property string  fontFamily: theme.defaultFont.family
    property bool    fontBold: false
    property bool    fontItalic: false
    property int     fontSize: theme.defaultFont.mSize.height
    property string  label: 'N/A'
    property string  labelColor: normalColor
    
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
            leftMargin: 10
            rightMargin: 10
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
            
            console.log(fontBold, fontItalic)
        })
    }
    
    PlasmaCore.DataSource {
        id: temperatureDataSource
        engine: "systemmonitor"
        interval: main.interval
        connectedSources: ['lmsensors/coretemp-isa-0000/Core_0']

        onNewData: {
            setTemperatureValue(data.value)
        }
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
            label = 'N/A'
        }
    }
    
    function formatValue(value) {
        var units = plasmoid.readConfig('units')
        var symbol  = 'C'
        switch (units) {
            case 0:
            default:
                symbol = 'C'
                break
            case 1:
                value = Math.ceil(value * 9/5.0 + 32)
                symbol = 'F'
                break
        }
        
        if (plasmoid.formFactor == 3) { // vertical
            symbol = '';
        }
        
        return value + '°' + symbol
    }
}