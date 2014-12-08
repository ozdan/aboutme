<%inherit file="base.mako"/>
<%block name="title">Гости вашей страницы</%block>
<%block name="content">
    <div id="user-list">
    %if len(user_list):
        % for user in user_list:
            <div class="user-in-list">
                <a href="${request.route_url('user', username=user['guest_username'])}">
                    ${user['guest_first_name']} ${user['guest_last_name']}
                </a> заходил ${user['time'].strftime('%d.%m.%Y')} в ${user['time'].strftime('%H:%M')}
            </div>
        % endfor
    %else:
        <h3>К вам никто не заходил :(</h3>
    %endif
    </div>
</%block>