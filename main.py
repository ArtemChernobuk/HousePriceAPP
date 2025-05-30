import flet as ft
import inference
import pandas as pd
import datetime
import os
import sqlite3

def run_base_sql(base_sql_path, db_path):
  if not os.path.exists(db_path):
    try:
      conn = sqlite3.connect(db_path)
      cursor = conn.cursor()

      with open(base_sql_path, 'r') as f:
        sql_script = f.read()

      cursor.executescript(sql_script)
      conn.commit()

    except Exception as e:


      if conn:
        conn.close()




# Пример использования:
base_sql_path = 'base.sql'
db_path = 'base.db'

run_base_sql(base_sql_path, db_path)


def main(page: ft.Page):
    # Настройки страницы
    page.title = "House Prices"
    page.window_icon = "./assets/favicon.png"
    page.padding = 10
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO

    # Цветовая палитра
    BG_COLOR = "#121212"
    BLACK_ACCENT = "#000000"
    WHITE_TEXT = "#FFFFFF"
    CARD_COLOR = "#1E1E1E"
    CHIP_COLOR = "#2E2E2E"
    CHIP_SELECTED_COLOR = "#424242"

    page.bgcolor = BG_COLOR

    def amenity_selected(e):
        # Изменяем цвет чипа при выборе
        if e.control.selected:
            e.control.bgcolor = CHIP_SELECTED_COLOR
        else:
            e.control.bgcolor = CHIP_COLOR
        page.update()

    # Функция для создания стилизованных элементов
    def create_text_field(label, prefix,  password=False):
        return ft.TextField(
            label=label,
            border_color=BLACK_ACCENT,
            focused_border_color=BLACK_ACCENT,
            color=WHITE_TEXT,
            cursor_color=WHITE_TEXT,
            label_style=ft.TextStyle(color=WHITE_TEXT),
            bgcolor=CARD_COLOR,
            password=password,
            can_reveal_password=password,
            suffix_text=prefix
        )

    def create_dropdown(label, options):
        return ft.Dropdown(
            label=label,
            options=[ft.dropdown.Option(opt) for opt in options],
            border_color=BLACK_ACCENT,
            focused_border_color=BLACK_ACCENT,
            color=WHITE_TEXT,
            label_style=ft.TextStyle(color=WHITE_TEXT),
            bgcolor=CARD_COLOR,
            expand=True,
        )

    def create_checkbox(label):
        return ft.Checkbox(
            label=label,
            fill_color=BLACK_ACCENT,
            check_color=WHITE_TEXT,
            expand=True,
        )

    # Создаем текстовое поле с автодополнением
    district_field = ft.TextField(
        label="Район",
        border_color=BLACK_ACCENT,
        focused_border_color=BLACK_ACCENT,
        color=WHITE_TEXT,
        cursor_color=WHITE_TEXT,
        label_style=ft.TextStyle(color=WHITE_TEXT),
        bgcolor=CARD_COLOR,
        expand=True
    )

    autocomplete = ft.Column(
        controls=[
            district_field,
            ft.ListView(
                controls=[
                    ft.ListTile(title=ft.Text("Вариант 1")),
                    ft.ListTile(title=ft.Text("Вариант 2"))
                ],
                visible=False
            )
        ]
    )

    title = ft.Row([ft.Icon(ft.Icons.HOTEL_CLASS), ft.Text("Amenities")])
    amenities = ["Подземная парковка", "Продаётся с мебелью", "Мусоропровод"]
    amenity_chips = []
    for amenity in amenities:
        amenity_chips.append(
            ft.Chip(
                label=ft.Text(amenity, color=WHITE_TEXT),
                bgcolor=CHIP_COLOR,
                selected_color=CHIP_SELECTED_COLOR,
                check_color=WHITE_TEXT,
                disabled_color=ft.Colors.GREY_700,
                autofocus=True,
                on_select=amenity_selected,
                shape=ft.RoundedRectangleBorder(radius=8),
                # shadow=ft.BoxShadow(
                #     spread_radius=0,
                #     blur_radius=5,
                #     color=BLACK_ACCENT,
                #     offset=ft.Offset(0, 2),
                # ),
            )
        )

    year_dropdown = ft.Dropdown(
        label="Год постройки",
        options=[ft.dropdown.Option(str(year)) for year in range(1900, 2025)],
        border_color=BLACK_ACCENT,
        focused_border_color=BLACK_ACCENT,
        color=WHITE_TEXT,
        label_style=ft.TextStyle(color=WHITE_TEXT),
        bgcolor=CARD_COLOR,
        expand=True,
    )

    # Основные элементы формы
    series_check = create_checkbox("Индивидуальный проект")
    checkbox_newsletter = create_checkbox("Подписаться на рассылку")
    checkbox_notifications = create_checkbox("Получать уведомления")
    checkbox_terms = create_checkbox("Принимаю условия использования")

    # Выпадающие меню
    bathroom = create_dropdown(
        "Санузел",
        ["1 совмещенный", "1 раздельный", "3 совмещенных",]
    )

    view = create_dropdown(
        "Вид из окон",
        ["Во двор", "На улицу", "На улицу и двор",]
    )

    repair = create_dropdown(
        "Ремонт",
        ["Без ремонта", "Косметический", "Евроремонт"]
    )

    type_house = create_dropdown(
        "Тип дома",
        ["Кирпичный", "Панельный", "Монолитный"]
    )

    type_overlap = create_dropdown(
        "Тип перекрытий",
        ["Деревянные", "Железобетонные", "Монолитный", "Смешанные"]
    )

    balcony = create_dropdown(
        "Балкон/лоджия",
        ["1 балкон", "2 балкона",  "1 лоджия", "2 лоджии", "1 лоджия, 1 балкон"]
    )

    elevators = create_dropdown(
        "Количество лифтов",
        ["1 пассажирский", "2 пассажирских",  "1 грузовой", "1 пассажирский, 1 грузовой"]
    )

    # Поля ввода
    house_number = create_text_field("Номер дома", "")
    area_field = create_text_field("Общая площадь", "м²")
    area_kitchen_field = create_text_field("Площадь кухни", "м²")
    floor_field = create_text_field("Этаж квартиры", "")
    floor_house_field = create_text_field("Всего этажей в доме", "")
    roof_field = create_text_field("Высота потолков", "м")
    series = create_text_field("Строительная серия", "")
    entrance = create_text_field("Подъезды", "")

    # Обработчик изменения состояния чекбокса
    def series_check_changed(e):
        series.disabled = series_check.value
        if series_check.value:
            series.value = ""
        page.update()

    series_check.on_change = series_check_changed

    submit_button = ft.ElevatedButton(
        "Отправить",
        bgcolor=BLACK_ACCENT,
        color=WHITE_TEXT,
        elevation=5,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=20,
        ),
    )
    load = ft.AlertDialog(
        modal=True,
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(
                        width=50,
                        height=50,
                        stroke_width=5,
                        color=CHIP_SELECTED_COLOR,
                    ),
                    ft.Text("Обрабатываем ваш запрос...", size=16, color=WHITE_TEXT),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Центрирование по горизонтали
                alignment=ft.MainAxisAlignment.CENTER,  # Центрирование по вертикали
                tight=True,
                expand=True,  # Растягиваем Column на весь Container
            ),
            width=300,
            height=250,
            alignment=ft.alignment.center,  # Центрирование содержимого Container
            padding=ft.padding.all(20),
        ),
        bgcolor=CARD_COLOR,
        shape=ft.RoundedRectangleBorder(radius=10),
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Цена недвижимости"),
        content=ft.Text("Do you really want to delete all those files?"),
        actions=[
            ft.TextButton("Ok", on_click=lambda e: page.close(dlg)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def submit_click(e):
        page.open(load)
        # Собираем все данные из формы
        form_data = {
            "Общая площадь": area_field.value,
            "Площадь кухни": area_kitchen_field.value,
            "Этаж квартиры": floor_field.value,
            "Всего этажей в доме": floor_house_field.value,
            "Год постройки": year_dropdown.value,
            "Высота потолков": roof_field.value,
            "Санузел": bathroom.value,
            "Вид из окон": view.value,
            "Ремонт": repair.value,
            "Индивидуальный проект": series_check.value,
            "Строительная серия": series.value,
            "Тип дома": type_house.value,
            "Подъезды": entrance.value,
            "Тип перекрытий": type_overlap.value,
            "Балкон/лоджия": balcony.value,
            "Количество лифтов": elevators.value,
            "Удобства": [chip.label.value for chip in amenity_chips if chip.selected],
        }
        room_mapping = {
            "Студия": 0,
            "1к": 1,
            "2к": 2,
            "3к": 3,
            "4к": 4
        }

        data = pd.DataFrame({
            "time": [str(datetime.datetime.now())],
            "Общая площадь": [float(area_field.value.replace(',', '.') if area_field.value else 0)],
            "Площадь кухни": [float(area_kitchen_field.value.replace(',', '.') if area_kitchen_field.value else 0)],
            "Этаж": [float(floor_field.value if floor_field.value else 0)],
            "Всего этажей": [float(floor_field.value if floor_field.value else 0)],
            "Год постройки": [float(year_dropdown.value if year_dropdown.value else 0)],
            "Высота потолков": [float(roof_field.value.replace(',', '.') if roof_field.value else 0)],
            "Санузел": [str(bathroom.value if bathroom.value else 0)],
            "Вид из окон": [str(view.value if view.value else 0)],
            "Ремонт": [str(repair.value if repair.value else 0)],
            "Строительная серия": [str(
                "Индивидуальный проект" if series_check.value else (series.value if series.value else 0))],
            "Тип дома": [str(type_house.value if type_house.value else 0)],
            "Тип перекрытий": [str(type_overlap.value if type_overlap.value else 0)],
            "Подъезды": [float(entrance.value) if entrance.value else 0],
            "Балкон/лоджия": [str(balcony.value if balcony.value else 0)],
            "Количество лифтов": [str(elevators.value if elevators.value else 0)],
            "Мусоропровод": [float(
                "Мусоропровод" in [chip.label.value for chip in amenity_chips if
                                   chip.selected] if amenity_chips else [])],
            "Подземная парковка": [float(
                "Подземная парковка" in [chip.label.value for chip in amenity_chips if
                                         chip.selected] if amenity_chips else [])],
            "Продаётся с мебелью": [float(
                "Продаётся с мебелью" in [chip.label.value for chip in amenity_chips if
                                          chip.selected] if amenity_chips else [])],
            "Количество комнат": [float(room_mapping.get(deal_type.controls[-1].value, 0))],
            # Added deal_type
            "Район": [str(district_field.value if district_field.value else 0)],  # Added autocomplete
            "Номер дома": [float(house_number.value if house_number.value else 0)],  # Added house_number
        })

        dlg.content =  ft.Text(str(inference.inference_model(data)))
        page.close(load)
        page.open(dlg)

        # # Выводим данные в консоль
        # print("\n=== Данные формы ===")
        # for key, value in form_data.items():
        #     print(f"{key}: {value}")
        # print("==================\n")

    # Привязываем функцию к кнопке
    submit_button.on_click = submit_click

    def create_radio_group(label, options):
        # Создаем RadioGroup
        radio_group = ft.RadioGroup(content=ft.Column())

        radio_buttons = []

        for option in options:
            btn_container = ft.Container(
                content=ft.Text(option, color=WHITE_TEXT, text_align=ft.TextAlign.CENTER),
                bgcolor=CHIP_COLOR,
                border_radius=8,
                border=ft.border.all(2, "transparent"),
                padding=15,
                alignment=ft.alignment.center,
                on_click=lambda e, opt=option: select_option(opt),
                width=150,  # Фиксированная ширина кнопки
            )

            radio = ft.Radio(value=option, visible=False)

            radio_buttons.append(ft.Stack([
                btn_container,
                radio
            ]))

            radio_group.content.controls.append(radio)

        def select_option(option):
            radio_group.value = option
            update_styles()

        def update_styles():
            for i, stack in enumerate(radio_buttons):
                container = stack.controls[0]
                is_selected = radio_group.value == options[i]
                container.border = ft.border.all(2, CHIP_SELECTED_COLOR if is_selected else "transparent")
                container.bgcolor = CHIP_SELECTED_COLOR if is_selected else CHIP_COLOR
            page.update()

        if options:
            radio_group.value = options[0]
            update_styles()

        return ft.Column(
            controls=[
                ft.Text(label, color=WHITE_TEXT),
                ft.Container(
                    content=ft.Row(
                        controls=radio_buttons,
                        spacing=10,
                        scroll=ft.ScrollMode.AUTO,  # Добавляем прокрутку если не помещается
                    ),
                    expand=True,  # Растягиваем контейнер на всю ширину
                    padding=ft.padding.symmetric(horizontal=10),  # Отступы по бокам
                ),
                radio_group
            ],
            spacing=10,
        )
    deal_type = create_radio_group(
        "Количество комнат",
        ["Студия", "1к", "2к", "3к", "4к "]
    )




    form = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Форма для подсчета цены квартиры", size=24, weight="bold", color=WHITE_TEXT),
                ft.Divider(height=10, color="transparent"),

                # Секция с полями ввода
                ft.Text("Укажите следующие значения:", color=WHITE_TEXT, size=18),
                ft.Text("Укажите район квартиры", color=WHITE_TEXT, size=16),
                autocomplete,
                house_number,
                area_field,
                area_kitchen_field,
                deal_type,
                ft.Row(
                    controls=[
                        ft.Container(
                            content=floor_field,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Text("из", color=WHITE_TEXT, size=18),
                            padding=ft.padding.only(top=15),
                        ),
                        ft.Container(
                            content=floor_house_field,
                            expand=True,
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                ),
                year_dropdown,
                roof_field,
                bathroom,
                view,
                repair,
                series_check,
                series,
                type_house,
                entrance,
                type_overlap,
                balcony,
                elevators,

               # Адаптивный ряд с чипами
                # Замените текущий ft.Row(amenity_chips) на:
                ft.Row(
                    amenity_chips,
                    wrap=True,  # Включает перенос на новую строку
                    spacing=10,  # Расстояние между элементами
                    run_spacing=10,  # Расстояние между строками
                ),
                ft.Divider(height=20, color=BLACK_ACCENT),
                submit_button
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START,
        ),
        width=1000,
        padding=30,
        border_radius=15,
        bgcolor=CARD_COLOR,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK54,
            offset=ft.Offset(0, 5),
        )
    )
    # Добавьте этот код после формы
    footer_content = ft.ResponsiveRow(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Совет:", size=16, weight="bold", color=WHITE_TEXT),
                        ft.Text("Для точного результата указывайте реальные параметры. Например, объективно оцените состояние ремонта — это действительно 'евроремонт' или просто хорошее состояние? Чем точнее данные, тем достовернее будет оценка.", size=14, color=WHITE_TEXT),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=20,
                border_radius=10,
                bgcolor=CARD_COLOR,
                col={"sm": 12, "md": 6},
                # На мобильных занимает всю ширину (12 колонок), на средних экранах - половину (6 колонок)
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Ограничение ответственности", size=16, weight="bold", color=WHITE_TEXT),
                        ft.Text("Используя информацию с HousePrice, помните, что окончательные решения остаются за вами. Мы не можем нести ответственность за действия, совершённые на основе данных нашего портала.", size=14, color=WHITE_TEXT),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=20,
                border_radius=10,
                bgcolor=CARD_COLOR,
                col={"sm": 12, "md": 6},
                # На мобильных занимает всю ширину (12 колонок), на средних экранах - половину (6 колонок)
            ),
        ],
        spacing=20,
        width=form.width,
    )

    # Обновите ваш основной контейнер
    main_content = ft.Column(
        controls=[
            form,
            footer_content,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Замените page.add(form) на:
    page.add(main_content)


ft.app(
    target=main,
    view=ft.WEB_BROWSER,
    assets_dir="assets",
    port=8000

)