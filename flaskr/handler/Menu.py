import json

from flask import current_app as app
from flask import abort, g, redirect, request, jsonify
from werkzeug.exceptions import abort
from flaskr import db
from flaskr.model.Menu import Menu, MenuSchema
from flaskr.utils.err import InvalidUsage
from flaskr.utils.auth import role_required

schema = MenuSchema()
schemas = MenuSchema(many=True)


@role_required(["admin"])
def findAndCountAll():
    """查询多条信息"""
    page_num = int(request.args.get('pageNum', '1'))
    page_size = int(request.args.get('pageSize', '10'))
    # sorter = request.args.getlist('sorter', None)
    data = Menu.query.paginate(
        page=page_num, per_page=page_size, error_out=False)
    return {
        "count": data.total,
        "rows": schemas.dump(data.items),
        # "rows": [item.to_dict() for item in data.items]
    }


@role_required(["admin"])
def singleCreate():
    """创建单条信息"""
    kwds = request.get_json()
    app.logger.info(f'用户提交数据：{kwds}')  # 记录提交的数据
    item = Menu(**kwds)
    db.session.add(item)
    db.session.commit()
    return schema.dump(item)


@role_required(["admin"])
def bulkUpdate():
    """更新多条信息"""
    ids = request.args.getlist('id')
    if len(ids) == 0:
        abort(400, "ID参数不能为空")
    kwds = request.get_json()
    app.logger.info(f'用户提交数据：{ids} - {kwds}')  # 记录提交的数据
    items = [Menu.query.get(id) for id in ids]
    for item in items:
        item.update(**kwds)
    db.session.commit()
    return {
        "rows": schemas.dump(items)
    }


@role_required(["admin"])
def bulkDestroy():
    """删除多条信息"""
    ids = request.args.getlist('id')
    if len(ids) == 0:
        abort(400, "ID参数不能为空")
    items = [Menu.query.get(id) for id in ids]
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return {
        "count": len(ids)
    }


def findByPk(id):
    """根据主键查询单条信息"""
    # item = Menu.query.get(id)
    # if item is None:
    #     abort(404, description="记录不存在")
    item = Menu.query.get_or_404(id)
    return schema.dump(item)


def updateByPk(id):
    """更新单条"""
    item = Menu.query.get_or_404(id)
    kwds = request.get_json()
    item.update(**kwds)
    db.session.commit()
    return schema.dump(item)


@role_required(["admin"])
def destroyByPk(id):
    """删除单条"""
    item = Menu.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return schema.dump(item)


@role_required(["admin"])
def bulkCreate():
    """创建多条信息"""
    kwds_list = request.get_json()
    app.logger.info(f'用户提交数据：{kwds_list}')  # 记录提交的数据
    items = [Menu(**kwds) for kwds in kwds_list]
    db.session.add_all(items)
    db.session.commit()
    return {
        "rows": schemas.dump(items)
    }