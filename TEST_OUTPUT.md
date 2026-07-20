# pytest result 

system> python manage.py test shipping.tests.test_models
Found 6 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
----------------------------------------------------------------------
Ran 6 tests in 0.008s

OK
Destroying test database for alias 'default'...
(venv) PS C:\Users\ADMIN\OneDrive\Documents\Desktop\Django1\Assingment\box_selection_system> python manage.py test shipping.tests.test_services
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 0.013s

OK
Destroying test database for alias 'default'...
(venv) PS C:\Users\ADMIN\OneDrive\Documents\Desktop\Django1\Assingment\box_selection_system> python manage.py test shipping.tests.test_api
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 0.020s

OK
Destroying test database for alias 'default'...

## coverage report

(venv) PS C:\Users\ADMIN\OneDrive\Documents\Desktop\Django1\Assingment\box_selection_system> coverage report
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
config\__init__.py                        0      0   100%
config\settings.py                       20      0   100%
config\urls.py                            3      1    67%
manage.py                                11      6    45%
shipping\__init__.py                      0      0   100%
shipping\admin.py                        28     15    46%
shipping\apps.py                          4      0   100%
shipping\migrations\0001_initial.py       7      0   100%
shipping\migrations\__init__.py           0      0   100%
shipping\models.py                       62     26    58%
shipping\serializers.py                  77     54    30%
shipping\services\box_selector.py        45      9    80%
shipping\tests\__init__.py                0      0   100%
shipping\tests\test_api.py               19      1    95%
shipping\tests\test_models.py            29      4    86%
shipping\tests\test_services.py          25      0   100%
shipping\urls.py                          3      0   100%
shipping\views.py                        50     18    64%
---------------------------------------------------------
TOTAL                                   383    134    65%

## Black (Code Formatter)

reformatted shipping/views.py
reformatted shipping/services/recommendation.py

All done! ✨ 🍰 ✨

## Flake8 (Linting)

.\venv\Lib\site-packages\setuptools\package_index.py:683:80: E501 line too long (81 > 79 characters)


