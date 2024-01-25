<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body id="author-form-page">

<br>
<form method="POST" action="?">
<table border="0" width="100%">
    <tr>
        <td></td>
        <td width="500px">
            <table border="0" width="100%">
                <tr>
                    <td>
                        <table border="0" width="100%">
                            <tr>
                                <td>
                                    <?php include 'menu.html' ?>
                                </td>
                            </tr>
                        </table>
                        <br><br>
                    </td>
                </tr>
                <tr>
                    <td>
                        <table align="center" border="0" width="350px">
                            <tr align="right">
                                <td width="20%"><label>Eesnimi: </label></td>
                                <td align="left"><input type="text" name="firstName"></td>
                            </tr>
                            <tr align="right">
                                <td width="20%"><label>Perekonnanimi: </label></td>
                                <td align="left"><input type="text" name="lastName"></td>
                            </tr>
                            <tr align="right">
                                <td><label>Hinne: </label></td>
                                <td align="left">
                                    <label><input type="radio" name="grade" value="1">1</label>
                                    <label><input type="radio" name="grade" value="2">2</label>
                                    <label><input type="radio" name="grade" value="3">3</label>
                                    <label><input type="radio" name="grade" value="4">4</label>
                                    <label><input type="radio" name="grade" value="5">5</label>
                                </td>
                            </tr>
                            <tr>
                                <td></td>
                                <td>
                                    <br>
                                    <button type="submit" name="submitButton"
                                            value="author-add">Salvesta</button>
                                </td>
                            </tr>
                        </table>
                        <hr>
                    </td>
                </tr>
                <tr>
                    <td>
                        <footer>
                            ICD0007 Näidisrakendus
                        </footer>
                    </td>
                </tr>
            </table>
        </td>
        <td></td>
    </tr>
</table>
</form>
</body>
</html>