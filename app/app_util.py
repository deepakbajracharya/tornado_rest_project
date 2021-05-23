def widget2Dict(widget):
    return {
        "id"              : widget.id,
        "name"            : widget.name,
        "number_of_parts" : widget.number_of_parts,
        "created_date"    : widget.created_date.isoformat(),
        "updated_date"    : widget.updated_date.isoformat()
    }
