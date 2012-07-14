Model
=====

class queryset_client.client.model_gen(\**configs).Model(\**kwargs)

    Bases: object

    **delete()**
        - Return type:  NoneType

    **save()**
        - Return type:  NoneType

    **schema(\*attrs)**

        * attrs example ::

            >>> self.schema("fields")
            # out fields schema
            >>> self.schema("fields", "id")
            # out id schema

        - Parameters:  attrs (tuple)
        - Return type:  dict
        - Returns:  model schema
