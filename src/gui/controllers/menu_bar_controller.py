from ..views.menu_bar import *

class MenuBarController():
    def __init__(self,menu_bar: MenuBar,projects):
        self.menu_bar = menu_bar
        self.collapsed_width = 100
        self.expanded_width = 200

        self.projects = projects
        self._create_projects()

        self.menu_bar.cbox_projects.currentIndexChanged.connect(
            self.menu_bar.menu_layout.setCurrentIndex
        )
        self.menu_bar.cbox_projects.currentTextChanged.connect(self.set_active_project)

        self.menu_bar.get_menu_button().clicked.connect(self.toggle_width)

        self.menu_bar.cbox_projects.setCurrentIndex(0)
        self.active_project = self.menu_bar.cbox_projects.currentText()

    def _create_projects(self):
        for project in self.projects:
            self.menu_bar.create_project_menu(project)

    def set_active_project(self,project_name):
        self.active_project = project_name

    def add_menu_items(self,menu_items,project_name):
        for menu_item in menu_items:
            self.menu_bar.add_menu_item(menu_item,project_name)
    
    def get_project_items(self,project_name = None):
        if project_name:
            return self.menu_bar.project_items[project_name]
        else:
            return self.menu_bar.project_items
    def toggle_width(self): 
        current_width = self.menu_bar.width()
        target_width = self.expanded_width if current_width == self.collapsed_width else self.collapsed_width

        group = QParallelAnimationGroup(self.menu_bar)

        self.animation = QPropertyAnimation(self.menu_bar,b"size")
        self.animation.setDuration(500)
        self.animation.setStartValue(QSize(current_width, self.menu_bar.height()))
        self.animation.setEndValue(QSize(target_width, self.menu_bar.height()))
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.valueChanged.connect(
            lambda size: self.menu_bar.setFixedWidth(size.width())
        )

        group.addAnimation(self.animation)

        for widget in self.menu_bar.get_widgets_to_animate():
            widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            widget.setMinimumWidth(0)
            widget.setMaximumWidth(widget.sizeHint().width())

            animation = QPropertyAnimation(widget,b"maximumWidth")
            animation.setDuration(500)
            animation.setEasingCurve(QEasingCurve.InOutQuad)

            if target_width == self.expanded_width:
                animation.setStartValue(0)
                animation.setEndValue(widget.sizeHint().width())
            else:
                animation.setStartValue(widget.width())
                animation.setEndValue(0)
            
            group.addAnimation(animation)

        for item in self.menu_bar.project_items[self.active_project]["items"]:
            lbl = item.lbl_text
            lbl.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            lbl.setMinimumWidth(0)
            lbl.setMaximumWidth(lbl.sizeHint().width())

            anim = QPropertyAnimation(lbl,b"maximumWidth")
            anim.setDuration(500)
            anim.setEasingCurve(QEasingCurve.InOutQuad)

            if target_width == self.expanded_width:
                anim.setStartValue(0)
                anim.setEndValue(lbl.sizeHint().width())
            else:
                anim.setStartValue(lbl.width())
                anim.setEndValue(0)
            
            group.addAnimation(anim)

        group.start()
        self.anim_group = group

    def get_default_widgets(self):
        return self.menu_bar.default_widgets
    
    def get_project_menu(self,project):
        return self.menu_bar.project_items[project]['widget']