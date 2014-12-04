<%inherit file="base.mako"/>
<%block name="title">Пользователь ${user.first_name} ${user.last_name}</%block>
<%block name="content">
<div id="concrete-user">
    <p>${user.first_name} ${user.last_name}</p>
    % if user.biography:
        <p>Биография: ${user.biography}</p>
    % endif
    % if user.location:
        <p>Местоположение: ${user.location}</p>
    % endif
    % if user.work:
        <p>Работа: ${user.work}</p>
    % endif
    % if user.education:
        <p>Образование: ${user.education}</p>
    % endif
    % if user.interest:
        <p>Интересы: ${user.interest}</p>
    % endif
</div>
</%block>