%UserProfile%\.pyenv\pyenv-win\versions\3.6.0\python.exe -m pip install --upgrade pip setuptools  wheel
%UserProfile%\.pyenv\pyenv-win\versions\3.7.0\python.exe -m pip install --upgrade pip setuptools  wheel
%UserProfile%\.pyenv\pyenv-win\versions\3.8.0\python.exe -m pip install --upgrade pip setuptools  wheel
%UserProfile%\.pyenv\pyenv-win\versions\3.9.0\python.exe -m pip install --upgrade pip setuptools  wheel
%UserProfile%\.pyenv\pyenv-win\versions\3.10.0\python.exe -m pip install --upgrade pip setuptools  wheel
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"
pushd ..
%UserProfile%\.pyenv\pyenv-win\versions\3.6.0\python.exe setup.py bdist_wheel -d wheelhouse
%UserProfile%\.pyenv\pyenv-win\versions\3.7.0\python.exe setup.py bdist_wheel -d wheelhouse
%UserProfile%\.pyenv\pyenv-win\versions\3.8.0\python.exe setup.py bdist_wheel -d wheelhouse
%UserProfile%\.pyenv\pyenv-win\versions\3.9.0\python.exe setup.py bdist_wheel -d wheelhouse
%UserProfile%\.pyenv\pyenv-win\versions\3.10.0\python.exe setup.py bdist_wheel -d wheelhouse
popd
