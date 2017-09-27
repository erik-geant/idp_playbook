<?php

$config = array(

    'admin' => array(
        'core:AdminPassword',
    ),

    'default-sp' => array(
        'saml:SP',
        'entityID' => null,
        'idp' => null,
        'discoURL' => null,
    ),

    'example-userpass' => array(
        'exampleauth:UserPass',

        'myname:hackme' => array(
            'uid' => array('myuid'),
            'eduPersonAffiliation' => array('member', 'student'),
            'mail'=> array('me@nowhere.xyz'),
            'TAL:federated_user_id' => array("tal-1234"),
            'grouperGroups' => array('employee', 'student', 'human'),
        )

    )

);
