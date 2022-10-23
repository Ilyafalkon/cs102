<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <style type="text/css">
   TR.good {
    background: #DBFFD8;
   }
   TR.maybe {
    background: #EEEEEE;
   }
   TR.never{
    background: #FFE1E8;
   }
  </style>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>#Likes</th>
                <th colspan="3">Label</th>
            </thead>
            <tbody>
                %for good_row in good_rows:
                <tr class="good">
                    <td><a href="{{ good_row.url }}">{{ good_row.title }}</a></td>
                    <td>{{ good_row.author }}</td>
                    <td>{{ good_row.points }}</td>
                    <td class="positive"><a href="/add_label/?whence=classify&label=good&id={{ good_row.id }}">Интересно</a></td>
                    <td class="active"><a href="/add_label/?whence=classify&label=maybe&id={{ good_row.id }}">Возможно</a></td>
                    <td class="negative"><a href="/add_label/?whence=classify&label=never&id={{ good_row.id }}">Не интересно</a></td>
                </tr>
                %end
                %for maybe_row in maybe_rows:
                <tr class="maybe">
                    <td><a href="{{ maybe_row.url }}">{{ maybe_row.title }}</a></td>
                    <td>{{ maybe_row.author }}</td>
                    <td>{{ maybe_row.points }}</td>
                    <td class="positive"><a href="/add_label/?whence=classify&label=good&id={{ maybe_row.id }}">Интересно</a></td>
                    <td class="active"><a href="/add_label/?whence=classify&label=maybe&id={{ maybe_row.id }}">Возможно</a></td>
                    <td class="negative"><a href="/add_label/?whence=classify&label=never&id={{ maybe_row.id }}">Не интересно</a></td>
                </tr>
                %end
                %for never_row in never_rows:
                <tr class="never">
                    <td><a href="{{ never_row.url }}">{{ never_row.title }}</a></td>
                    <td>{{ never_row.author }}</td>
                    <td>{{ never_row.points }}</td>
                    <td class="positive"><a href="/add_label/?whence=classify&label=good&id={{ never_row.id }}">Интересно</a></td>
                    <td class="active"><a href="/add_label/?whence=classify&label=maybe&id={{ never_row.id }}">Возможно</a></td>
                    <td class="negative"><a href="/add_label/?whence=classify&label=never&id={{ never_row.id }}">Не интересно</a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/fit" class="ui right floated small primary button">Retrain the algorithm</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>