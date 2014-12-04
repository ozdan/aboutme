<%inherit file="base.mako"/>
<%block name="title">Добро пожаловать на персональный сайт пользователей!</%block>
<%block name="content">
    <div id="index">
        <h2>Добро пожаловать на персональный сайт пользователей!</h2>
        <p>Пожалуйста, <a href="${request.route_url('login')}">войдите</a> или\
            <a href="${request.route_url('registration')}">зарегистрируйтесь</a></p>
    </div>
</%block>