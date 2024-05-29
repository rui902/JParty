from PyQt6.QtCore import QLoggingCategory

qt_context_log = QLoggingCategory("QFont")
qt_context_log.setFilterRules("*.debug=false")
qt_context_log.setFilterRules("*.info=false")
qt_context_log.setFilterRules("*.warn=false")
qt_context_log.setFilterRules("*.warning=false")
