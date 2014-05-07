import QtQuick 1.0
import org.kde.plasma.core 0.1 as PlasmaCore

Item {
    id: root
    
    property int     minimumWidth: 48
    property int     minimumHeight: 48
    property int     interval: 1000
    property string  normalColor: theme.textColor
    property string  overheatColor: '#f00'
    property int     overheatLevel: 80
    property int     units: 0
    property string  unitsSign: 'C'
    property string  sensor: ''
    property string  fontFamily: ''
    property int     fontSize: 1
    
    PlasmaCore.Theme {
        id: theme
    }
    
    Text: {
        id: text
        text: '0°' + unitsSign
        color: normalColor
        height: 48
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignTop
        font {
            family: fontFamily
            pointSize: fontSize
        }
    }
    
    property Component compactRepresentation: {
        text: 'aaaa'
    }
    
    Component.onCompleted: {
        plasmoid.addEventListener('ConfigChanged', function () {
            var font = plasmoid.readConfig('font')
            
            print ('font: ' + font)
            
            fontFamily = font.toString().split(',')[0]
            print('font family: ' + fontFamily)
            
            fontSize = font.toString().split(',')[1]
            print('font size: ' + fontSize)
            
            interval = plasmoid.readConfig('interval')
            print('interval: ' + interval)
            
            normalColor = plasmoid.readConfig('normalColor')
            print('normal color: ' + normalColor)
            
            overheatColor = plasmoid.readConfig('overheatColor')
            print('overheat color: ' + overheatColor)
            
            overheatLevel = plasmoid.readConfig('overheatLevel')
            print('overheat level: ' + overheatLevel)
            
            units = plasmoid.readConfig('units')
            print('units: ' + units)
            
            sensor = plasmoid.readConfig('sensor')
            print('sensor: ' + sensor)
            
            if (units == 1) {
                unitsSign = 'F'
            }
            print('units sign: ' + unitsSign)
        })
    }
    
    PlasmaCore.DataSource {
        id: tDataSource
        engine: "systemmonitor"
        interval: 1000

        onSourceAdded: {
            disconnectSource(source)
            connectSource(source)
        }
        
        onNewData: {
            if (sourceName == 'lmsensors/coretemp-isa-0000/Physical_id_0') {
                setTemperatureValue(data.value)
            }
        }
    }
    
    function setTemperatureValue(value) {
        if (value) {
            var value = Math.ceil(value)
            if (value > overheatLevel) {
                text.color = overheatColor
            } else {
                text.color = normalColor
            }
    
            
            if (units == 1) {
                value = Math.ceil(value * 9/5.0 + 32)
            }
            text.text = value + '°' + unitsSign
        }
    }
}