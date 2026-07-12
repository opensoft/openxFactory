WITH protected(role_name) AS (
  VALUES
    ('xfactory_v2_runtime'),
    ('xfactory_v2_control'),
    ('xfactory_v2_audit')
), attributes AS (
  SELECT
    role_name,
    rol.rolsuper,
    rol.rolcreatedb,
    rol.rolcreaterole,
    rol.rolreplication,
    rol.rolbypassrls
  FROM protected
  LEFT JOIN pg_roles AS rol ON rol.rolname = role_name
)
SELECT bool_and(
  NOT rolsuper
  AND NOT rolcreatedb
  AND NOT rolcreaterole
  AND NOT rolreplication
  AND NOT rolbypassrls
)
AND NOT EXISTS (
  SELECT 1
  FROM pg_auth_members membership
  JOIN pg_roles member_role ON member_role.oid = membership.member
  JOIN pg_roles granted_role ON granted_role.oid = membership.roleid
  WHERE member_role.rolname IN (
    'xfactory_v2_runtime', 'xfactory_v2_control', 'xfactory_v2_audit',
    'hcs_customer_a', 'hcs_customer_b', 'hcs_install_admin',
    'hcs_control_plane', 'hcs_audit'
  )
  AND granted_role.rolname IN ('xfactory_v2_owner', 'xfactory_v2_migrator')
)
FROM attributes;
