<%
    def authenticated():
        return request.authenticated_userid is not None
%>

<html>
    <head>
        <title><%block name="title"></%block></title>
        <link href="${request.static_url('aboutme:static/style.css')}" rel="stylesheet">
    </head>
    <body>
    <a href="${request.route_url('home')}"><img src="${request.static_url('aboutme:static/home.jpg')}"/></a>
    % if authenticated():
    <div id="logout">
        <a href="${request.route_url('user', username=request.authenticated_userid)}">Моя страница</a>
        <a href="${request.route_url('logout')}">Выйти</a>
    </div>
    % endif
    <%block name="content">

    </%block>
    </body>
</html>