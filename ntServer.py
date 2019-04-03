from networktables import NetworkTables

NetworkTables.initialize(server="10.17.26.2")

preferences = NetworkTables.getTable("Preferences")

preferences.putNumber("Vision/H/Lower", 0)
preferences.putNumber("Vision/H/Upper", 255)
preferences.putNumber("Vision/S/Lower", 0)
preferences.putNumber("Vision/S/Upper", 255)
preferences.putNumber("Vision/L/Lower", 0)
preferences.putNumber("Vision/L/Upper", 255)