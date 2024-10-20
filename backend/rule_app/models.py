from django.db import models

class ASTNode(models.Model):
    NODE_TYPE_CHOICES = [
        ('operator', 'Operator'),
        ('operand', 'Operand')
    ]
    
    type = models.CharField(max_length=10, choices=NODE_TYPE_CHOICES, null =True)
    value = models.CharField(max_length=255, null=True, blank=True)
    left = models.ForeignKey('self', null=True, blank=True, related_name='left_child', on_delete=models.CASCADE)
    right = models.ForeignKey('self', null=True, blank=True, related_name='right_child', on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
        }

class Rule(models.Model):
    name = models.CharField(max_length=100, null = True)
    root_node = models.OneToOneField(ASTNode, on_delete=models.CASCADE, related_name='rule', null= True)  # Add related_name for reverse access
    rule_string = models.TextField(null = True)
    ast_representation = models.TextField(null = True)

    def __str__(self):
        return f"Rule(name={self.name}, rule_string={self.rule_string})"


class UserData(models.Model):
    age = models.IntegerField()
    department = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.IntegerField()
