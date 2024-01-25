<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Päevi alla valitud piiri</title>
    <link href="pages/styles.css" rel="stylesheet">
</head>
<body>

<?php include 'menu.html' ?>

<h5>Mitu päeva oli valitud aastal temperatuur alla valitud piiri?</h5>

<form method="POST" action="?">
    <table>
        <tr>
            <td><label for="year">Aasta</label>:</td>
            <td>
                <select name="year" id="year">
                    <option>2019</option>
                    <option>2020</option>
                    <option>2021</option>
                </select>
            </td>
        </tr>
        <tr>
            <td><label for="temp">Temperatuur</label>:</td>
            <td>
                <input type="number" name="temp" id="temp">
            </td>
        </tr>
        <tr>
            <td></td>
            <td>
                <br>
                <button type="submit" name="command"
                        value="days-under-temp">Arvuta</button>
            </td>
        </tr>
    </table>
</form>

</body>
</html>