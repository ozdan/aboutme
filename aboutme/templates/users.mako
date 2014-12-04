<%inherit file="base.mako"/>
<%block name="title">Список пользователей</%block>
<%block name="content">
    <div id="user-list">
    % for user in user_list:
        <div class="user-in-list">
            <a href="${request.route_url('user', username=user.username)}">${user.first_name} ${user.last_name}</a>
        </div>
    % endfor
    </div>
</%block>
