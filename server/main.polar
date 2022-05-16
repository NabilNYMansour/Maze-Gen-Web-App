allow(actor, action, resource) if
  has_permission(actor, action, resource);

actor User {}

resource Maze {
    permissions = ["read", "create", "delete"];
    roles = ["viewer", "creator", "admin"];

    "read" if "viewer";
    "create" if "creator";
    "delete" if "admin";

    "viewer" if "creator";
    "creator" if "admin";
}

has_role(actor: User, role_name: String, _maze: Maze) if
    actor.role = role_name;

has_permission(actor: User, "read", _maze: Maze) if
    actor.role = "viewer";

has_permission(actor: User, "create", _maze: Maze) if
    actor.role = "creator";

# >>> admin = User(username="admin", role="admin")
# >>> creator = User(username="creator", role="creator")
# >>> viewer = User(username="viewer", role="viewer")
# >>> db.session.add_all([admin, creator, viewer])
# >>> db.session.commit()