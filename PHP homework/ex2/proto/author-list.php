<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body id="author-list-page">

<br>
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
                    </td>
                </tr>
                <tr>
                    <td>
                        <table border="0" width="100%">
                            <tr>
                                <td align="left" width="40%">Eesnimi</td>
                                <td width="50%">Perekonnanimi</td>
                                <td width="10%">Hinne</td>
                            </tr>
                        </table>
                        <hr>
                    </td>
                </tr>
                <tr>
                    <td>
                        <table border="0" width="100%">
                            <?php print addAuthors() ?>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <br>
                        <table border="0" width="100%">
                            <tr>
                                <td>
                                    <footer>
                                        ICD0007 Näidisrakendus
                                    </footer>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </td>
        <td></td>
    </tr>
</table>
</body>
</html>