<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body id="book-form-page">

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
                                <td width="20%"><label>Pealkiri: </label></td>
                                <td align="left"><input type="text" name="title"></td>
                            </tr>
<!--                            <tr align="right">-->
<!--                                <td width="20%"><label>Autor 1: </label></td>-->
<!--                                <td align="left">-->
<!--                                    <select id="author1" name="author1">-->
<!--                                        <option value="">&nbsp;</option>-->
<!--                                        <option value="1">Alo Ansberg</option>-->
<!--                                        <option value="2">Mart Mets</option>-->
<!--                                    </select>-->
<!--                                </td>-->
<!--                            </tr>-->
<!--                            <tr align="right">-->
<!--                                <td><label>Autor 2: </label></td>-->
<!--                                <td align="left">-->
<!--                                    <select id="author2" name="author2">-->
<!--                                        <option value="">&nbsp;</option>-->
<!--                                        <option value="1">Mari Mets</option>-->
<!--                                        <option value="2">Kari Mets</option>-->
<!--                                    </select>-->
<!--                                </td>-->
<!--                            </tr>-->
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
                            <tr align="right">
                                <td><label>Loetud: </label></td>
                                <td align="left">
                                    <label><input type="checkbox" name="isRead"></label>
                                </td>
                            </tr>
                            <tr>
                                <td></td>
                                <td>
                                    <br>
                                    <button type="submit" name="submitButton"
                                            value="book-add">Salvesta</button>
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