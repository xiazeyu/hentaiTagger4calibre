mkdir out
cd work
for /d %%i in (*) do (cd "%%i"&&7z a -r -scsUTF-8 -mx6 -mmt6 "z.zip"&&move "z.zip" "../../out/%%i.zip"&&cd ..)
@pause